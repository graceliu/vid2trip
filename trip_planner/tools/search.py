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
 
"""Wrapper to Youtube Search Grounding."""

from duckduckgo_search import DDGS
from google.adk.tools import ToolContext
import logging

logger = logging.getLogger(__name__)

def search_videos(query: str, tool_context: ToolContext):
    """
    Searches for videos using DuckDuckGo (which returns clean YouTube links) 
    and returns a formatted list of results.
    
    Args:
        query: The search query (e.g. "Things to do in Tokyo"). 
        tool_context: The ADK tool context.
    """
    # Clean the query if the agent added "site:youtube.com"
    clean_query = query.replace("site:youtube.com", "").strip()
    
    logger.debug(f"[Tool] Searching for videos: {clean_query}...")
    
    
    try:
        # 1. Use DuckDuckGo Video Search
        # max_results controls how many we fetch
        results = DDGS().videos(
            keywords=clean_query,
            max_results=5,
            safesearch="moderate",
            region="wt-wt",
        )
        
        if not results:
            return "No videos found."

        # 2. Format the output
        formatted_results = []
        for video in results:
            # DDGS returns keys: 'title', 'description', 'content' (which is the URL), 'duration'
            title = video.get('title', 'Unknown Title')
            link = video.get('content', 'No Link') # 'content' is the direct URL
            duration = video.get('duration', 'N/A')
            
            # Filter for YouTube links only (just in case)
            if "youtube.com" in link or "youtu.be" in link:
                formatted_results.append(f"- **{title}** ({duration}) - Link: {link}")
            
        if not formatted_results:
            return "No valid YouTube links found."

        return "\n".join(formatted_results)

    except Exception as e:
        return f"Error performing video search: {str(e)}"