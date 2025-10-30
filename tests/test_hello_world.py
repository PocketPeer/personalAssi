import importlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_hello_world_says_hello_world():
    hello_world = importlib.import_module("hello_world")
    assert hello_world.say_hello() == "Hello, world!"
