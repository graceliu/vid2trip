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
class StateManager:
    """
    A simple in-memory store to hold the latest state for each user.
    Used solely for the 'Abandon & Resume' hydration feature.
    """
    def __init__(self):
        # Format: { "user_id": { "destination": "Tokyo", ... } }
        self._user_latest_state = {}

    def save_user_state(self, user_id: str, state: dict):
        """Snapshots the current state dictionary for a user."""
        if user_id:
            self._user_latest_state[user_id] = state.copy()

    def get_user_state(self, user_id: str):
        """Retrieves the last known state for a user."""
        return self._user_latest_state.get(user_id, {})

# Global Singleton
state_manager = StateManager()