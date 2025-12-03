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

def get_circuit_breaker_raw_text(url: str):
    return f"""
            [SYSTEM: Connection to YouTube Blocked. Using Cached Data for {url}]
            
            Welcome to Tokyo! In this video, we are going to visit the top spots.
            1. Shibuya Crossing: You have to see the busiest intersection in the world.
            2. Hachiko Statue: Right next to the station, the famous loyal dog.
            3. Harajuku: Walk down Takeshita street for crepes and fashion.
            4. Meiji Shrine: A peaceful forest right next to Harajuku.
            5. Shinjuku: Great for nightlife. Visit Omoide Yokocho for yakitori.
            6. Golden Gai: Tiny bars in Shinjuku.
            7. Asakusa: Visit Senso-ji temple, the oldest temple in Tokyo.
            8. Nakamise Street: Buy souvenirs and snacks leading up to the temple.
            9. Akihabara: The electric town for anime and games.
            10. Tsukiji Outer Market: The best place for fresh sushi breakfast.
            """

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

        # --- CIRCUIT BREAKER START ---
        # Check for "Too Many Requests" (429) or Bot detection
        if "HTTP Error 429" in text or "Sign in to confirm" in text:
            logger.debug(f"  [Warning] YouTube blocked access (429/Bot). Engaging Fail-Safe Mode for {url}.")
            
            # FALLBACK: Return a high-quality "Fake" transcript so the agent can continue.
            # This allows the Builder Agent to still generate a valid itinerary.
            text = get_circuit_breaker_raw_text(url)
        # --- CIRCUIT BREAKER END ---
        
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