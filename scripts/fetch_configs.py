#!/usr/bin/env python3
"""
Fetch VPN configurations from URLs and save them locally
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# Configuration
CONFIGS_DIR = "configs"
VPNMIRRORS_DIR = "VPNMIRRORS"
URLS_FILE = "urls.txt"
METADATA_FILE = "vpn_metadata.json"

# Create directories
Path(CONFIGS_DIR).mkdir(exist_ok=True)
Path(VPNMIRRORS_DIR).mkdir(exist_ok=True)

def get_filename_from_url(url):
    """Extract filename from URL or generate one"""
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename or '.' not in filename:
        # Generate filename based on domain and timestamp
        domain = parsed.netloc.replace('.', '_')
        filename = f"{domain}_{datetime.now().strftime('%Y%m%d_%H%M')}.ovpn"
    return filename

def fetch_config(url, retry_count=3):
    """Fetch a single VPN configuration with retry"""
    for attempt in range(retry_count):
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.content, response.status_code
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Attempt {attempt + 1}/{retry_count} failed: {str(e)}")
            if attempt == retry_count - 1:
                return None, None
    return None, None

def save_config(filename, content, source_url):
    """Save configuration file and metadata"""
    # Save to VPNMIRRORS
    vpn_path = os.path.join(VPNMIRRORS_DIR, filename)
    config_path = os.path.join(CONFIGS_DIR, filename)
    
    try:
        with open(vpn_path, 'wb') as f:
            f.write(content)
        with open(config_path, 'wb') as f:
            f.write(content)
        
        file_size = len(content)
        print(f"  ✅ Saved: {filename} ({file_size} bytes)")
        
        return {
            "filename": filename,
            "size": file_size,
            "source_url": source_url,
            "download_link": f"https://raw.githubusercontent.com/{os.environ.get('GITHUB_REPOSITORY', 'user/repo')}/main/{VPNMIRRORS_DIR}/{filename}",
            "saved_at": datetime.now().isoformat(),
            "status": "success"
        }
    except Exception as e:
        print(f"  ❌ Error saving {filename}: {str(e)}")
        return {
            "filename": filename,
            "source_url": source_url,
            "status": "failed",
            "error": str(e)
        }

def load_urls(urls_file):
    """Load URLs from file"""
    urls = []
    try:
        with open(urls_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)
        print(f"✅ Loaded {len(urls)} URLs from {urls_file}")
        return urls
    except FileNotFoundError:
        print(f"⚠️  File not found: {urls_file}")
        return []

def main():
    print("=" * 60)
    print("🔄 VPN Configuration Fetcher")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S MSK')}")
    print("=" * 60)
    
    # Load URLs
    urls = load_urls(URLS_FILE)
    if not urls:
        print("❌ No URLs to fetch")
        return False
    
    # Fetch configurations
    metadata = {
        "fetch_time": datetime.now().isoformat(),
        "total_urls": len(urls),
        "successful": 0,
        "failed": 0,
        "configs": []
    }
    
    for url in urls:
        content, status_code = fetch_config(url)
        
        if content:
            filename = get_filename_from_url(url)
            config_info = save_config(filename, content, url)
            metadata["configs"].append(config_info)
            
            if config_info["status"] == "success":
                metadata["successful"] += 1
            else:
                metadata["failed"] += 1
        else:
            metadata["failed"] += 1
            metadata["configs"].append({
                "source_url": url,
                "status": "failed",
                "error": "Could not fetch"
            })
    
    # Save metadata
    try:
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Metadata saved to {METADATA_FILE}")
    except Exception as e:
        print(f"❌ Error saving metadata: {str(e)}")
        return False
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"  Total URLs: {metadata['total_urls']}")
    print(f"  Successful: {metadata['successful']}")
    print(f"  Failed: {metadata['failed']}")
    print(f"  Success Rate: {(metadata['successful']/metadata['total_urls']*100):.1f}%")
    print("=" * 60)
    
    return metadata['successful'] > 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
