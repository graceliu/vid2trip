# Copyright 2025 Google LLC
# Copyright 2025 Grace Liu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The 'youtube_transcript_api' tool for several agent to obtain transcript for youtube video."""

import os
import glob
import logging
import yt_dlp
import uuid
from google.adk.tools import ToolContext
import logging
import tempfile
import os

PROXY_URL = os.environ.get("YT_PROXY_URL")

logger = logging.getLogger(__name__)

def get_youtube_transcript(video_url: str, tool_context: ToolContext = None):
    """
    Retrieves the transcript from a YouTube video URL using yt-dlp.
    This method is robust against YouTube's bot detection.
    Saving to /tmp to avoid Read-Only filesystem errors in Cloud.
    """
    # Use the system temp directory (usually /tmp in Linux/Cloud)
    temp_dir = tempfile.gettempdir()
    temp_id = str(uuid.uuid4())
    
    # Define the full path pattern for the output
    # yt-dlp appends .en.vtt automatically, so we just give the prefix
    output_template = os.path.join(temp_dir, f"temp_subs_{temp_id}")
    
    # Configure yt-dlp to only download subtitles, not the video
    ydl_opts = {
        'skip_download': True,      # Don't download the video file
        'writeautomaticsub': True,  # Download auto-generated subs
        'writesubtitles': True,     # Download manual subs if available
        'sub_langs': ['en', 'en-orig', '.*'],   # Prefer English, but accept others
        'outtmpl': output_template,  # <--- Write to /tmp
        'quiet': True,              # Less noise in console
        'no_warnings': True,
        # CRITICAL: Also move the cache to /tmp so it doesn't try to write to ~
        'paths': {'home': temp_dir},
    }

    if PROXY_URL:
        ydl_opts['proxy'] = PROXY_URL
        logger.debug(f"[Tool] Using Proxy for {video_url}...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.debug(f"[Tool]  ... Fetching subs for {video_url} ...")
            ydl.download([video_url])

        # yt-dlp saves files like '/tmp/temp_subs_<id>.en.vtt'
        # We search specifically in the temp_dir
        search_pattern = os.path.join(temp_dir, f"temp_subs_{temp_id}*.vtt")
        list_of_files = glob.glob(search_pattern)
        
        if not list_of_files:
            return f"Skipped: No subtitles found for {video_url}"

        # Use the first file found (usually English if available)
        vtt_file = list_of_files[0]
        
        # Read and clean the VTT file
        transcript_text = _parse_vtt(vtt_file)
        
        # Clean up: Delete the temporary file
        try:
            os.remove(vtt_file)
        except OSError:
            pass

        return transcript_text

    except Exception as e:
        # Debugging: Return the actual error so we can see it in the Agent response
        return f"Error retrieving transcript: {str(e)}"

def _parse_vtt(file_path):
    """
    Simple helper to strip timestamps and metadata from a WebVTT file.
    """
    lines = []
    seen_lines = set() # To remove duplicates common in auto-subs
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines, 'WEBVTT' header, and timestamps (arrows)
                if not line: continue
                if 'WEBVTT' in line: continue
                if '-->' in line: continue
                if line.isdigit(): continue # Skip raw line numbers
                
                # Deduplicate lines (auto-captions often repeat phrases)
                if line not in seen_lines:
                    lines.append(line)
                    seen_lines.add(line)
        
        full_text = " ".join(lines)
        
        # Truncate if too long for LLM
        if len(full_text) > 15000:
            full_text = full_text[:15000] + "... (truncated)"
            
        return full_text
        
    except Exception as e:
        return f"Error parsing subtitle file: {e}"