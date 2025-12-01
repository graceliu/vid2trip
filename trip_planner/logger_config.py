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
import logging
import sys
import os
from dotenv import load_dotenv

import logging
import sys
import os
from dotenv import load_dotenv

def setup_logging():
    """
    Configures the Global Root Logger.
    """
    load_dotenv()
    
    env_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, env_level_str, logging.INFO)

    # 1. Get the ROOT logger (no name provided)
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # 2. Clear default handlers (Vertex/Cloud Run often adds a default one)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 3. Create a clean Console Handler for Cloud Logging
    # Using sys.stdout ensures it lands in the "stdout" stream in Log Explorer
    c_handler = logging.StreamHandler(sys.stdout)
    c_handler.setLevel(numeric_level)
    
    # 4. Use a format that is easy to grep in Cloud Logs
    c_format = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
    c_handler.setFormatter(c_format)

    root_logger.addHandler(c_handler)

    # 5. Silence chatty third-party libraries (Optional but recommended for DEBUG)
    # If you don't do this, 'DEBUG' will show you every HTTP request Google makes.
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("google.auth").setLevel(logging.WARNING)
    logging.getLogger("fsspec").setLevel(logging.WARNING)

    # 6. Test it immediately
    root_logger.info(f"Logging configured at level: {env_level_str}")
    
    return root_logger