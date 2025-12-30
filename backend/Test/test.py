import sys
from pathlib import Path

# Add the project root to the path so we can import from backend
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.calculate import sum_numbers

def test_sum_numbers():
    assert sum_numbers(1, 2) == 1
    assert sum_numbers(-1, 1) == 0
    assert sum_numbers(0, 0) == 0
