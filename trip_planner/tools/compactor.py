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
from google.genai import Client
import logging

logger = logging.getLogger(__name__)

def compact_travel_ideas(tool_context: ToolContext):

    # Initialize client specifically for this tool
    client = Client()

    """
    Reads raw video transcripts from 'ideas_raw_text', extracts 
    high-value travel POIs, and saves them to 'ideas_refined_text'.
    
    This separates the 'noise' of the video from the 'signal' of the trip plan.
    """
    state = tool_context.state
    raw_texts = state.get("ideas_raw_text", []) # We will rename the input key
    
    if not raw_texts:
        return "No raw transcripts found to compact."

    logger.debug(f"\n[Tool] Compacting {len(raw_texts)} transcripts using Gemini...")
    
    # Initialize output list
    state["ideas_refined_text"] = []
    
    success_count = 0
    
    for i, transcript in enumerate(raw_texts):
        # Skip if empty or error message
        if not transcript or transcript.startswith("Skipped") or len(transcript) < 50:
            continue
            
        logger.debug(f"  ... Processing transcript #{i+1}...")
        
        prompt = f"""
        You are a Data Distiller. Convert this raw YouTube transcript into structured travel notes.
        
        INPUT TRANSCRIPT:
        {transcript[:30000]} # Truncate for safety
        
        INSTRUCTIONS:
        1. Extract specific Places of Interest (Name, Type, Why go there).
        2. Extract specific Food/Drink recommendations.
        3. Ignore host chatter, intros, outros, and sponsor reads.
        4. Output format: Bullet points.
        """
        
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            # Tag the source for the Builder Agent
            compacted_entry = f"--- Source {i+1} ---\n{response.text}"
            state["ideas_refined_text"].append(compacted_entry)
            success_count += 1
            
        except Exception as e:
            logger.debug(f"  [Error] Compaction failed for #{i+1}: {e}")
            # Fallback: Pass raw text if AI fails, so we don't lose data
            state["ideas_refined_text"].append(transcript[:5000])

    # CRITICAL OPTIMIZATION: Free up the memory!
    # We replace the massive raw text list with an empty list or None.
    logger.debug("  [Tool] Optimization: Clearing raw transcripts from memory.")
    state["ideas_raw_text"] = []

    return f"Success: Compacted {success_count} transcripts into structured notes."