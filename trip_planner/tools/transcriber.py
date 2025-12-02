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

from google.adk.tools import ToolContext
from trip_planner.tools.youtube import get_youtube_transcript

import logging

logger = logging.getLogger(__name__)

def transcribe_videos(tool_context: ToolContext):
    """
    Batch processes all videos currently in the 'ideas_videos' list.
    Extracts transcripts and saves them to 'ideas_raw_text'.
    
    Args:
        tool_context: The ADK context containing the session state.
    """
    state = tool_context.state
    video_urls = state.get("ideas_videos", [])
    
    if not video_urls:
        return "No videos found to transcribe."
        
    logger.debug(f"[Tool] Starting batch transcription for {len(video_urls)} videos...")
    
    transcribed_count = 0
    errors = []
    
    # Initialize the list if it doesn't exist
    if "ideas_raw_text" not in state:
        state["ideas_raw_text"] = []
        
    for url in video_urls:
        # 1. Call your existing robust yt-dlp function
        # Note: We call the function directly, not as a tool
        text = get_youtube_transcript(url, tool_context)
        
        if text.startswith("Skipped:") or text.startswith("Error"):
            errors.append(f"{url}: {text}")
            continue
            
        # 2. Save to memory directly
        state["ideas_raw_text"].append(text)
        transcribed_count += 1
        logger.debug(f"[Tool]  - Transcribed: {url}")
    
    # Return a more detailed summary
    if errors:
        error_summary = "\n".join(errors)
        return f"Partial Success: Transcribed {transcribed_count} videos. Failures:\n{error_summary}"

    return f"Success: Transcribed {transcribed_count} videos. {len(errors)} failed."