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
from google.adk.agents.callback_context import CallbackContext
from trip_planner.state_manager import state_manager
from trip_planner.tools.memory import _load_precreated_scenario
import logging

logger = logging.getLogger(__name__)

# --- PRE-HOOK (Hydrate) ---
async def hydrate_session_state(callback_context: CallbackContext):
    """
    PRE-HOOK: Runs BEFORE the agent sees the prompt.
    """
    # Update all references inside the function:
    user_id = "default_user"
    
    if not callback_context.state.get("destination"):
        logger.debug(f"\n[System] 💧 Looking for user state to hydrate...")
        saved_state = state_manager.get_user_state(user_id)
        
        if saved_state and saved_state.get("destination"):
            logger.debug(f"\n[System] 💧 Hydrating user state...")
            callback_context.state.update(saved_state)
            callback_context.state._value["_just_restored"] = True

# --- POST-HOOK (Persist) ---
async def persist_session_state(callback_context: CallbackContext):
    """
    POST-HOOK: Runs AFTER every turn.
    Saves the state so we can restore it later.
    """
    user_id = "default_user"
    
    # 1. Consume the flash flag if present
    # Access ._value to use the standard dictionary .pop() method
    if callback_context.state.get("_just_restored"):
        callback_context.state._value.pop("_just_restored", None)

    # 2. Access internal ._value to get the raw dictionary
    # This avoids the KeyError: 0 crash in the ADK State wrapper
    state_as_dict = callback_context.state._value.copy()

    # 3. Save the dictionary
    state_manager.save_user_state(user_id, state_as_dict)
    
    # 4. Save History

    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session)
    
    logger.debug(f"  [Memory] 💾 Snapshot saved for user '{user_id}'")


async def root_agent_pre_hook(callback_context: CallbackContext):
    """
    Master Pre-Hook.
    """
    try:
        _load_precreated_scenario(callback_context) 
    except Exception:
        pass

    await hydrate_session_state(callback_context)