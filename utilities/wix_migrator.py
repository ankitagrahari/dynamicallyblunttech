import csv
import os
import re
import requests
import sys
import json
from datetime import datetime

# Prevent field overflow exceptions during compilation runs
csv.field_size_limit(sys.maxsize)

# CONFIGURATION
CSV_FILE = 'Posts.csv'
OUTPUT_DIR = 'content/posts'
IMAGE_DIR = 'static/images'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

def clean_slug(title, fallback_slug=""):
    if fallback_slug and isinstance(fallback_slug, str) and fallback_slug.strip():
        return fallback_slug.strip().lower()
    slug = title.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug

def parse_wix_image_uri_old_working(wix_url):
    """Transforms raw wix media URIs into standard high-res static download endpoints."""
    if not wix_url or not isinstance(wix_url, str):
        return None, None
        
    if wix_url.startswith('wix:image://v1/'):
        parts = wix_url.replace('wix:image://v1/', '').split('/')
        if parts:
            filename = parts[0]
            # Strip the signature suffix to isolate clean web file names
            clean_filename = re.sub(r'~mv2.*', '', filename)
            if not clean_filename.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.heic')):
                clean_filename += '.jpg'
            return f"https://static.wixstatic.com/media/{filename}", clean_filename
            
    elif 'wixstatic.com' in wix_url or wix_url.startswith('http'):
        filename = wix_url.split('/')[-1].split('?')[0].split('#')[0]
        clean_filename = re.sub(r'~mv2.*', '', filename)
        if not clean_filename.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.heic')):
            clean_filename += '.jpg'
            
        if 'media/' in wix_url:
            return wix_url, clean_filename
        else:
            return f"https://static.wixstatic.com/media/{filename}", clean_filename            
    return None, None

def parse_wix_image_uri(wix_url):
    """Transforms raw wix media URIs into standard high-res static download endpoints."""
    if not wix_url or not isinstance(wix_url, str):
        return None, None

    # Handle the native wix:image:// structure
    if wix_url.startswith('wix:image://v1/'):
        # Strip protocol string out
        path_payload = wix_url.replace('wix:image://v1/', '')
        # Split by forward slashes to isolate the image file hash payload
        # e.g., ['df024c_01c956...~mv2.jpg', 'filename.jpg#width=...']
        parts = path_payload.split('/')
        if len(parts) > 0:
            raw_id = parts[0]
            # Strip metadata out of the ID string if any exists
            raw_id = raw_id.split('#')[0].split('?')[0]
            
            # Clean up the output filename by stripping Wix sizing (~mv2...)
            clean_filename = re.sub(r'~mv2.*', '', raw_id)
            if not clean_filename.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.heic')):
                clean_filename += '.jpg'
                
            # Construct the absolute public download CDN endpoint
            download_url = f"https://static.wixstatic.com/media/{raw_id}"
            return download_url, clean_filename

    # Handle absolute web URLs that might already be in the data dump
    elif 'wixstatic.com' in wix_url or wix_url.startswith('http'):
        filename_segment = wix_url.split('/')[-1].split('?')[0].split('#')[0]
        clean_filename = re.sub(r'~mv2.*', '', filename_segment)
        if not clean_filename.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.heic')):
            clean_filename += '.jpg'
            
        # Isolate the file payload and rebuild the clean URL string
        raw_id = filename_segment
        download_url = f"https://static.wixstatic.com/media/{raw_id}"
        return download_url, clean_filename

    return None, None

def download_and_localize_image(img_input):
    """Downloads target graphics locally and translates references into clean relative Hugo routing paths."""
    url, filename = parse_wix_image_uri(img_input)
    if not url or not filename:
        return None
        
    local_path = os.path.join(IMAGE_DIR, filename)
    
    if not os.path.exists(local_path):
        try:
            print(f"📥 Fetching resource: {filename}")
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(r.content)
            else:
                print(f"⚠️ Failed HTTP download for: {url}")
                return None
        except Exception as e:
            print(f"❌ Exception downloading image {url}: {e}")
            return None
            
    return f"images/{filename}"

def extract_text_from_wix_json(node_data):
    """Recursively processes the true JSON architecture blocks down to native structural Markdown syntax."""
    markdown_out = ""
    
    if isinstance(node_data, dict):
        node_type = node_data.get('type')
        
        # 1. Base Leaf Text Elements
        if node_type == 'TEXT' and 'textData' in node_data:
            text_data = node_data['textData']
            text = text_data.get('text', '')
            decorations = text_data.get('decorations', [])
            
            # Identify internal structural markers
            is_bold = any(d.get('type') == 'BOLD' for d in decorations)
            is_italic = any(d.get('type') == 'ITALIC' for d in decorations)
            link_info = next((d.get('linkData', {}).get('link', {}) for d in decorations if d.get('type') == 'LINK'), None)
            
            # Format inline decorations
            if is_bold:
                text = f"**{text}**"
            if is_italic:
                text = f"*{text}*"
            if link_info and 'url' in link_info:
                sanitized_url = link_info['url'].strip("'\"").strip()
                text = f"[{text}]({sanitized_url})"
                
            markdown_out += text
            
        # 2. Structural Paragraph blocks
        elif node_type == 'PARAGRAPH':
            p_text = ""
            for child in node_data.get('nodes', []):
                p_text += extract_text_from_wix_json(child)
            if p_text.strip():
                markdown_out += f"\n\n{p_text}"
            
        # 3. Structural Headings
        elif node_type == 'HEADING':
            heading_data = node_data.get('headingData', {})
            # Read exact layout levels or default safely
            level = heading_data.get('level', 2)
            h_text = ""
            for child in node_data.get('nodes', []):
                h_text += extract_text_from_wix_json(child)
            if h_text.strip():
                markdown_out += f"\n\n{'#' * level} {h_text.strip()}"
                
        # 4. Embedded Source Code boxes
        elif node_type == 'CODE_BLOCK':
            code_text = ""
            for child in node_data.get('nodes', []):
                if child.get('type') == 'TEXT':
                    code_text += child.get('textData', {}).get('text', '')
                else:
                    code_text += extract_text_from_wix_json(child)
            markdown_out += f"\n\n```java\n{code_text.strip()}\n```"
            
        # 5. Direct Blockquotes
        elif node_type == 'BLOCKQUOTE':
            bq_text = ""
            for child in node_data.get('nodes', []):
                bq_text += extract_text_from_wix_json(child)
            lines = [f"> {line}" for line in bq_text.strip().split('\n') if line.strip()]
            markdown_out += f"\n\n" + "\n".join(lines)
            
        # 6. Inline Post Images
        elif node_type == 'IMAGE' and 'imageData' in node_data:
            img_src = node_data['imageData'].get('image', {}).get('src', {}).get('id', '')
            if img_src:
                local_path = download_and_localize_image(img_src)
                if local_path:
                    markdown_out += f"\n\n![Blog Illustration](/{local_path})"
                    
        # 7. Relational Tables
        elif node_type == 'TABLE':
            rows = node_data.get('nodes', [])
            table_markdown = "\n"
            for i, row in enumerate(rows):
                if row.get('type') == 'TABLE_ROW':
                    cell_texts = []
                    for cell in row.get('nodes', []):
                        cell_content = ""
                        for child in cell.get('nodes', []):
                            cell_content += extract_text_from_wix_json(child)
                        cell_texts.append(cell_content.strip().replace('\n', ' '))
                    
                    table_markdown += "\n| " + " | ".join(cell_texts) + " |"
                    
                    # Generate the separating rule right underneath header cells
                    if i == 0:
                        table_markdown += "\n| " + " | ".join(['---'] * len(cell_texts)) + " |"
            markdown_out += f"\n{table_markdown}\n"
            
        # 8. Unordered Lists
        elif node_type == 'BULLETED_LIST':
            for item in node_data.get('nodes', []):
                if item.get('type') == 'LIST_ITEM':
                    item_text = ""
                    for child in item.get('nodes', []):
                        item_text += extract_text_from_wix_json(child)
                    markdown_out += f"\n* {item_text.strip()}"
                    
        # Fallback recursive sweep for any unexpected containers
        elif 'nodes' in node_data:
            for child in node_data['nodes']:
                markdown_out += extract_text_from_wix_json(child)
                
    elif isinstance(node_data, list):
        for item in node_data:
            markdown_out += extract_text_from_wix_json(item)
            
    return markdown_out

# MASTER EXECUTION ROUTINE
with open(CSV_FILE, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        title = row.get('Title') or "Untitled Post"
        rich_content_raw = row.get('Rich Content') or ""
        published_date_str = row.get('Published Date') or ""
        slug_field = row.get('Slug') or ""
        cover_image_raw = row.get('Cover Image') or ""
        tags_raw = row.get('Tags') or ""
        categories_raw = row.get('Categories') or ""
        
        if not rich_content_raw:
            continue
            
        print(f"⚙️ Compiling parsed structures for: {title}")
        post_slug = clean_slug(title, fallback_slug=slug_field)
        
        # Format timestamps correctly
        try:
            parsed_date = datetime.strptime(published_date_str.split('.'), '%Y-%m-%d %H:%M:%S')
            hugo_date = parsed_date.strftime('%Y-%m-%dT%H:%M:%S+05:30')
        except:
            hugo_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+05:30')
            
        # Parse the JSON layout
        parsed_markdown_body = ""
        try:
            json_data = json.loads(rich_content_raw)
            parsed_markdown_body = extract_text_from_wix_json(json_data)
        except json.JSONDecodeError:
            parsed_markdown_body = rich_content_raw
            
        # Extract the cover image
        local_cover_path = ""
        if cover_image_raw:
            local_cover_path = download_and_localize_image(cover_image_raw)
            
        tags_list = [t.strip() for t in tags_raw.split(',') if t.strip()] if tags_raw else []
        categories_list = [c.strip() for c in categories_raw.split(',') if c.strip()] if categories_raw else []
        
        # CONSTRUCT HUGO METADATA
        front_matter = f'---\ntitle: "{title}"\ndate: {hugo_date}\ndraft: false\n'
        if local_cover_path:
            front_matter += f'featureImage: "{local_cover_path}"\n'
        if tags_list:
            front_matter += f'tags: {tags_list}\n'
        if categories_list:
            front_matter += f'categories: {categories_list}\n'
        front_matter += 'showReadingTime: true\n---\n\n'
        
        final_output = front_matter + parsed_markdown_body.strip()
        
        with open(os.path.join(OUTPUT_DIR, f"{post_slug}.md"), 'w', encoding='utf-8') as out_file:
            out_file.write(final_output)

print("✨ Success! Wix JSON editor payloads successfully unpacked into standard Markdown formatting.")
