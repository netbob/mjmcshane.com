#!/usr/bin/env python3
"""
WordPress XML to Jekyll/Chirpy converter
Extracts posts, pages, attachments from WordPress export XML and converts to Markdown.
"""

import xml.etree.ElementTree as ET
import re
import os
import html
import shutil
from pathlib import Path
from datetime import datetime

# Config
XML_FILE = '/home/.z/chat-uploads/michaelmcshane.wordpress.2026-04-15.000-d0787ff51c8f.xml'
UPLOADS_DIR = '/home/.z/chat-uploads/uploads'
JEKYLL_ROOT = '/home/workspace/mjmcshane.com'
WP_URL = 'https://mjmcshane.com'

# Chirpy uses _posts for blog posts, root for pages
POSTS_DIR = Path(JEKYLL_ROOT) / '_posts'
PAGES_DIR = Path(JEKYLL_ROOT)
ASSETS_DIR = Path(JEKYLL_ROOT) / 'assets' / 'img'

# Ensure dirs exist
POSTS_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# XML namespaces
NS = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
    'wfw': 'http://wellformedweb.org/CommentAPI/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'wp': 'http://wordpress.org/export/1.2/',
}

def decode_entities(text):
    """Decode HTML entities and unescape for XML."""
    if not text:
        return ''
    # Replace common WordPress entities
    text = text.replace('&#8211;', '–')  # en dash
    text = text.replace('&#8212;', '—')  # em dash
    text = text.replace('&#8216;', "'")   # left single quote
    text = text.replace('&#8217;', "'")   # right single quote
    text = text.replace('&#8220;', '"')   # left double quote
    text = text.replace('&#8221;', '"')   # right double quote
    text = text.replace('&#8230;', '…')   # ellipsis
    text = text.replace('&#038;', '&')    # ampersand
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    return text

def clean_html_to_markdown(content):
    """Convert basic HTML to Markdown."""
    if not content:
        return ''
    
    content = decode_entities(content)
    
    # WordPress captions: [caption id="..." align="..." width="..."]<img ...> caption text [/caption]
    content = re.sub(r'\[caption[^\]]*\](.*?)\[/caption\]', r'\1', content, flags=re.DOTALL)
    
    # WordPress more tag
    content = content.replace('<!--more-->', '')
    
    # Block editor: <!-- wp:xxx --> ... <!-- /wp:xxx -->
    content = re.sub(r'<!-- wp:[^/]+ -->\s*', '', content)
    content = re.sub(r'<!-- /wp:[^"]+ -->\s*', '', content)
    content = re.sub(r'<!-- wp:[/a-z]+ [^/]+ -->\s*', '', content)
    
    # Remove remaining HTML comments
    content = re.sub(r'<!--.*?-->\s*', '', content, flags=re.DOTALL)
    
    # Headings
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', content, flags=re.DOTALL)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', content, flags=re.DOTALL)
    content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n#### \1\n', content, flags=re.DOTALL)
    
    # Paragraphs
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
    
    # Blockquotes
    content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1\n\n', content, flags=re.DOTALL)
    
    # Line breaks
    content = content.replace('<br>', '\n')
    content = content.replace('<br/>', '\n')
    content = content.replace('<br />', '\n')
    
    # Bold/italic
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
    content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.DOTALL)
    
    # Links
    def replace_link(m):
        text = m.group(2) if m.group(2) else ''
        href = m.group(1)
        if href.startswith(WP_URL):
            href = href.replace(WP_URL, '')
        if text:
            return f'[{text}]({href})'
        return href
    content = re.sub(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', replace_link, content, flags=re.DOTALL)
    
    # Images - convert to Markdown, download if possible
    def replace_image(m):
        src = m.group(1)
        alt = m.group(2) or ''
        caption = m.group(3) or ''
        # Download image
        filename = download_image(src)
        if filename:
            return f'\n![{alt}](/assets/img/{filename}){caption}\n'
        return f'\n![{alt}]({src}){caption}\n'
    
    # wp:image blocks: <figure class="wp-block-image"><img src="..." alt="..."/></figure>
    content = re.sub(r'<figure class="wp-block-image[^"]*">\s*<img[^>]+src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/>\s*(?:<figcaption>(.*?)</figcaption>)?\s*</figure>', 
                    replace_image, content, flags=re.DOTALL)
    
    # Simple img tags
    content = re.sub(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/>', 
                    replace_image, content, flags=re.DOTALL)
    content = re.sub(r'<img[^>]+src=["\']([^"\']+)["\']*/>', 
                    lambda m: f'\n![]({m.group(1)})\n', content)
    
    # Lists
    content = re.sub(r'<ul[^>]*>(.*?)</ul>', r'\n\1\n', content, flags=re.DOTALL)
    content = re.sub(r'<ol[^>]*>(.*?)</ol>', r'\n\1\n', content, flags=re.DOTALL)
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', content, flags=re.DOTALL)
    
    # Code blocks
    content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.DOTALL)
    content = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```', content, flags=re.DOTALL)
    
    # Clean remaining tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Clean up whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()
    
    return content

def download_image(src):
    """Download an image from WordPress uploads to assets/img."""
    if not src or not src.startswith('http'):
        return None
    
    filename = src.split('/')[-1]
    # Remove query strings
    filename = re.sub(r'\?.*', '', filename)
    dest = ASSETS_DIR / filename
    
    if dest.exists():
        return filename
    
    try:
        import urllib.request
        # Map WP URL to local upload path
        if 'wp-content/uploads' in src:
            local_path = src.split('wp-content/uploads/')[-1]
            src_path = Path(UPLOADS_DIR) / local_path.split('/')[-1]
            # Find in uploads tree
            src_path = find_in_uploads(local_path)
            if src_path and src_path.exists():
                shutil.copy2(src_path, dest)
                print(f"  Copied: {filename}")
                return filename
    except Exception as e:
        print(f"  Failed to copy {src}: {e}")
    return None

def find_in_uploads(relative_path):
    """Find a file in uploads directory by partial path match."""
    filename = relative_path.split('/')[-1]
    for root, dirs, files in os.walk(UPLOADS_DIR):
        if filename in files:
            return Path(root) / filename
    return None

def parse_date(date_str):
    """Parse WordPress date string to Jekyll date format."""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return date_str

def get_item_date(item):
    """Get post date in various formats."""
    date_str = item.find('wp:post_date', NS).text or item.find('pubDate').text or ''
    return parse_date(date_str)

def get_slug(item):
    """Get post slug."""
    slug = item.find('wp:post_name', NS).text
    if not slug:
        # Generate from title
        title = item.find('title', NS).text or ''
        slug = re.sub(r'[^a-z0-9-]', '-', title.lower())
        slug = re.sub(r'-+', '-', slug).strip('-')
    return slug

def get_categories(item):
    """Extract categories as list."""
    cats = []
    for cat in item.findall('category'):
        domain = cat.get('domain', '')
        if domain == 'category':
            cats.append(cat.get('nicename', ''))
    return cats

def get_tags(item):
    """Extract tags as list."""
    tags = []
    for cat in item.findall('category'):
        domain = cat.get('domain', '')
        if domain == 'post_tag':
            tags.append(cat.get('nicename', ''))
    return tags

def generate_front_matter(item, post_type):
    """Generate YAML front matter."""
    title = decode_entities(item.find('title', NS).text or '')
    date = get_item_date(item)
    slug = get_slug(item)
    categories = get_categories(item)
    tags = get_tags(item)
    status = item.find('wp:status', NS).text
    
    fm = ['---']
    fm.append(f"title: \"{title}\"")
    fm.append(f"date: {date}")
    fm.append(f"categories: [{", ".join(categories)}]")
    if tags:
        fm.append(f"tags: [{", ".join(tags)}]")
    fm.append(f"permalink: /{slug}/")
    fm.append(f"published: {status == 'publish'}")
    fm.append("---")
    fm.append("")
    
    return '\n'.join(fm)

def process_posts(tree):
    """Process all posts and pages from the XML."""
    root = tree.getroot()
    channel = root.find('channel')
    
    posts_created = 0
    pages_created = 0
    attachments_found = 0
    
    for item in channel.findall('item'):
        post_type = item.find('wp:post_type', NS).text
        status = item.find('wp:status', NS).text
        title = item.find('title', NS).text or ''
        slug = get_slug(item)
        
        if post_type == 'attachment':
            attachments_found += 1
            # Download attachment
            content = item.find('content:encoded', NS).text or ''
            src_match = re.search(r'src=["\']([^"\']+)["\']', content)
            if src_match:
                download_image(src_match.group(1))
            continue
        
        if post_type not in ('post', 'page'):
            continue
        
        if status != 'publish':
            print(f"  Skipping {post_type}: {title} (status: {status})")
            continue
        
        content = item.find('content:encoded', NS).text or ''
        content = clean_html_to_markdown(content)
        
        front_matter = generate_front_matter(item, post_type)
        
        if post_type == 'post':
            # Jekyll posts must be named: YYYY-MM-DD-slug.md
            date_str = get_item_date(item)[:10]
            filename = f"{date_str}-{slug}.md"
            out_file = POSTS_DIR / filename
            posts_created += 1
        else:
            # Pages go to root or subdirectory
            filename = f"{slug}.md"
            out_file = PAGES_DIR / filename
            pages_created += 1
        
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(front_matter)
            f.write(content)
        
        print(f"  Created {post_type}: {filename}")
    
    print(f"\nSummary:")
    print(f"  Posts: {posts_created}")
    print(f"  Pages: {pages_created}")
    print(f"  Attachments: {attachments_found}")

def main():
    print(f"WordPress → Jekyll/Chirpy Migration")
    print(f"=" * 40)
    print(f"Source: {XML_FILE}")
    print(f"Uploads: {UPLOADS_DIR}")
    print(f"Target: {JEKYLL_ROOT}")
    print()
    
    # Parse XML
    print("Parsing XML...")
    tree = ET.parse(XML_FILE)
    print("Done parsing.")
    
    # Process items
    print("\nProcessing posts and pages...")
    process_posts(tree)
    
    # Copy important images
    print("\nCopying key images to assets/img...")
    key_images = [
        ('2018/08/Bolsa-Chica-July-2018.jpg', 'Bolsa-Chica-July-2018.jpg'),
    ]
    for upload_path, filename in key_images:
        src = find_in_uploads(upload_path.split('/')[-1])
        if src:
            shutil.copy2(src, ASSETS_DIR / filename)
            print(f"  Copied: {filename}")
    
    print("\n✓ Migration complete!")
    print(f"\nNext steps:")
    print(f"  1. Review generated files in _posts/ and root")
    print(f"  2. Update _config.yml with your site info")
    print(f"  3. Test locally: cd {JEKYLL_ROOT} && bundle exec jekyll serve")
    print(f"  4. Push to GitHub when ready")

if __name__ == '__main__':
    main()
