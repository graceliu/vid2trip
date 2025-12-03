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

"""Build itinerary agent. An agent that builds itinerary given a list of itinerary ideas raw text."""

from google.adk.agents import Agent
from trip_planner.sub_agents.build_itinerary import prompt
from trip_planner.tools.itinerary import save_itinerary # Import new tool
from trip_planner.tools.memory import memorize

build_itinerary_agent = Agent(
    model="gemini-2.5-pro",
    name="build_itinerary_agent", # Corrected name
    description="Builds an itinerary by discussing with the user, then saves it.",
    instruction=prompt.BUILD_ITINERARY_INSTR, 
    tools=[memorize, save_itinerary], 
)

