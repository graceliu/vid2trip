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

from typing import Any, Dict
from google.adk.tools import ToolContext
from trip_planner.shared_libraries.types import Itinerary
import logging

logger = logging.getLogger(__name__)

def save_itinerary(itinerary: Dict[str, Any], tool_context: ToolContext):
    """
    Finalizes the trip planning process by saving the structured itinerary.
    
    Args:
        itinerary: A JSON object representing the itinerary. 
                   IT MUST FOLLOW THIS EXACT SCHEMA:
                   {
                     "destination": "City Name",
                     "days": [
                       {
                         "day_number": 1,
                         "events": [
                           {
                             "event_type": "visit",  # or 'lunch', 'dinner'
                             "location": "Name of place",
                             "description": "Short description",
                             "address": "Address or area",
                             "start_time": "09:00",
                             "end_time": "11:00",
                             "booking_required": false
                           }
                         ]
                       }
                     ]
                   }
        tool_context: The ADK tool context.
    """
    logger.debug(f"[Tool] Validating itinerary...")

    try:
        # Validate that the LLM actually followed the instructions above
        validated_obj = Itinerary(**itinerary)
        itinerary_dict = validated_obj.model_dump()
    except Exception as e:
        # Return a helpful error message to the agent so it can self-correct
        return {"status": f"Error: You missed required fields. Please ensure every event has 'location', 'description', 'start_time', 'end_time', and 'address'. Details: {str(e)}"}
    
    tool_context.state['itinerary'] = itinerary_dict
    logger.debug(f"[Tool] Itinerary saved for {itinerary_dict.get('destination', 'Unknown')}")
    
    return {"status": "Itinerary saved successfully. Return control to root."}