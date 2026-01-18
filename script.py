import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from datetime import datetime

# Podcast metadata
PODCAST_TITLE = "Cum Town Archive"
PODCAST_LINK = "https://example.com"
PODCAST_DESCRIPTION = "Archive of Cum Town podcast episodes."
PODCAST_AUTHOR = "Cum Town"
PODCAST_IMAGE = "https://example.com/artwork.jpg"
PODCAST_LANGUAGE = "en-us"

# Base URL for GitHub audio files
BASE_URL = "https://github.com/user-attachments/files/"
START_NUMBER = 24698754  # first number in your sequence

XML_FILE = "episodes_metadata.xml"  # your XML metadata file
OUTPUT_FILE = "podcast.xml"

def format_rfc822(timestamp):
    dt = datetime.utcfromtimestamp(int(timestamp))
    return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")

# Parse XML metadata
tree = ET.parse(XML_FILE)
root = tree.getroot()

rss_items = []

for i, file in enumerate(root.findall('file')):
    # Increment the number for GitHub URL
    episode_number = START_NUMBER + i
    
    # MP3 filename (just the name part, not the full path)
    # Get the filename
    raw_filename = file.attrib['name'].split('/')[-1]

    # Replace spaces with dots to match GitHub URL
    filename = raw_filename.replace(' ', '.')
    audio_url = f"{BASE_URL}{episode_number}/{filename}"
    
    # Extract metadata
    title = escape(file.findtext('title', default='Untitled'))
    description = escape(file.findtext('comment', default=''))
    pub_date = format_rfc822(file.findtext('mtime', default='0'))

    # Build RSS item
    item = f"""
    <item>
      <title>{title}</title>
      <description>{description}</description>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{audio_url}" type="audio/mpeg"/>
      <itunes:explicit>false</itunes:explicit>
    </item>
    """
    rss_items.append(item.strip())

# Build full RSS feed
rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>{PODCAST_TITLE}</title>
    <link>{PODCAST_LINK}</link>
    <language>{PODCAST_LANGUAGE}</language>
    <description>{PODCAST_DESCRIPTION}RSSVERIFY</description>
    <itunes:author>{PODCAST_AUTHOR}</itunes:author>
    <itunes:explicit>false</itunes:explicit>
    <itunes:image href="{PODCAST_IMAGE}"/>
    {''.join(rss_items)}
  </channel>
</rss>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(rss_feed)

print(f"RSS feed generated: {OUTPUT_FILE}")
