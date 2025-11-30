import pathlib
import json
import dotenv
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator
from google.adk.evaluation.eval_config import EvalConfig

pytest_plugins = ("pytest_asyncio",)

@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()

@pytest.mark.asyncio
async def test_all():
    """Test the agent using the golden dataset and custom config."""
    
    base_dir = pathlib.Path(__file__).parent
    eval_set_path = base_dir / "data/trip_planner.evalset.json"

    # 3. Pass it to the evaluator
    await AgentEvaluator.evaluate(
        "trip_planner",          
        str(eval_set_path),      
        num_runs=1
    )