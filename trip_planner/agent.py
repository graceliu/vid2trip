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

from google.adk.agents import Agent

from trip_planner import prompt

from trip_planner.sub_agents.gather_videos.agent import gather_videos_agent
from trip_planner.sub_agents.build_itinerary.agent import build_itinerary_agent

from trip_planner.tools.memory import memorize
from trip_planner.tools.memory import _load_precreated_scenario
from trip_planner.tools.transcriber import transcribe_videos

from trip_planner.logger_config import setup_logging
setup_logging()

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="A Trip Planner using the services of multiple sub-agents",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        gather_videos_agent,
        build_itinerary_agent
    ],
    tools=[memorize, transcribe_videos],
    before_agent_callback=_load_precreated_scenario
)
