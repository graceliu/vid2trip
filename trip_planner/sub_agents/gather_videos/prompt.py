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

"""Prompt for gather videos agent."""


GATHER_VIDEOS_AGENT_INSTR = """
- Given a trip destination, you help the user curate a list of videos that represent the points of interest.
- Use the `search_videos` tool to search for videos.
- Simply pass the topic (e.g. "Top things to do in Tokyo") to the tool.
- Ask the user to review a list of videos and choose which videos they would like to add.
    - Present the list in a user-friendly bulleted, well formatted list.
- Use the `memorize_to_list` tool to store the user's chosen videos (URLs only) in `ideas_videos`.
- After storing the list of videos, return control back to the root agent.

# Context

Trip destination: {destination}
Trip ideas videos: {ideas_videos}
"""
