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

"""The 'memorize_to_list' and 'memorize' tools for several agents to affect session states."""

import json
import os
from typing import Dict, Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State

from google.adk.tools import ToolContext
from typing import List

from trip_planner.shared_libraries import constants

SAMPLE_SCENARIO_PATH = os.getenv(
    "TRIP_PLANNER_SCENARIO", "trip_planner/scenarios/empty_default.json"
)


def memorize_to_list(key: str, values: List[str], tool_context: ToolContext):
    """
    Memorize a list of items into a memory list.

    Args:
        key: the label indexing the memory list.
        values: A list of strings to be added.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    if key not in mem_dict:
        mem_dict[key] = []
    
    added_count = 0
    for val in values:
        if val not in mem_dict[key]:
            mem_dict[key].append(val)
            added_count += 1
            
    return {"status": f'Stored {added_count} new items in "{key}". Current list size: {len(mem_dict[key])}'}


def memorize(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information, one key-value pair at a time.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be stored.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    mem_dict[key] = value
    return {"status": f'Stored "{key}": "{value}"'}

def _set_initial_states(source: Dict[str, Any], target: State | dict[str, Any]):
    """
    Safely initializes session state. 
    Only sets values if the key is NOT present in the target state.
    """
    for key, value in source.items():
        # Option A: Only set if key is missing (Safe Init)
        if key not in target:
            target[key] = value
            
        # Option B: Or use setdefault (Pythonic way for dicts)
        # target.setdefault(key, value) 

def _load_precreated_scenario(callback_context: CallbackContext):
    """
    Sets up the initial state if not already present.
    """    
    # Optional: Check a flag to skip file I/O entirely after first run
    if callback_context.state.get("is_initialized"):
        return

    data = {}
    try:
        with open(SAMPLE_SCENARIO_PATH, "r") as file:
            data = json.load(file)
            print(f"\nLoading Initial State from {SAMPLE_SCENARIO_PATH}...\n")
    except FileNotFoundError:
        print(f"Warning: Scenario file not found at {SAMPLE_SCENARIO_PATH}")
        return

    _set_initial_states(data.get("state", {}), callback_context.state)
    
    # Mark as initialized so we don't reload the file every turn
    callback_context.state["is_initialized"] = True
