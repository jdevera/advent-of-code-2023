from pathlib import Path
from textwrap import dedent
import pytest
@pytest.fixture
def input_file_factory(tmp_path):
    """
    Creates a temporary input file with the given contents
    """
    def mkinput(content):
        assert content[0] == '\n'
        content = dedent(content)[1:]
        file = tmp_path / 'input'
        file.write_text(content)
        return file
    yield mkinput

@pytest.fixture
def day_input(request: pytest.FixtureRequest) -> Path:
    """
    Get the file called input that lives in the day module.
    This assumes tests are under a "test" module in the day folder
    """
    input_file = request.path.resolve().parent.parent / 'input'
    assert input_file.exists()
    yield input_file


