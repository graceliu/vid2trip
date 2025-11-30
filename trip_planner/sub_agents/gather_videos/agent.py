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

"""Gather videos agent. An agent gathering videos related to the trip destination."""

from google.adk.agents import Agent
from trip_planner.sub_agents.gather_videos import prompt
from trip_planner.tools.memory import memorize_to_list
from trip_planner.tools.search import search_videos

gather_videos_agent = Agent(
    model="gemini-2.5-flash",
    name="gather_videos_agent",
    description="Given a trip destination, this agent gathers videos related to the destination.",
    instruction=prompt.GATHER_VIDEOS_AGENT_INSTR,
    tools=[search_videos, memorize_to_list]
)
