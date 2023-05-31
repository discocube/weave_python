import pytest
import time
from unittest.mock import patch
from src import weave


@patch("weave.main.weave")  # Mock the weave function
def test_main(mock_weave):
    # Set up mock return value
    mock_solution = [(0, 0, 0), (0, 0, 2), (2, 0, 2), (2, 0, 0)]
    mock_weave.return_value = mock_solution

    # Replace print statements with capturing the output
    captured_output = []
    def mock_print(*args):
        captured_output.append(" ".join(map(str, args)))

    # Replace check_solution with a no-op
    def mock_check_solution(solution):
        pass

    # Patch print and check_solution functions
    with patch("builtins.print", side_effect=mock_print), \
         patch("weave.main.check_solution", side_effect=mock_check_solution):
        weave(50)

    # Assertions
    assert len(captured_output) == 1  # One line printed
    assert captured_output[0].startswith("4")  # Check the length of the solution


# Run the test
pytest.main()
