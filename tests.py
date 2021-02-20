import os, pathlib
import pytest

os.chdir( pathlib.Path.cwd() / 'app' )

pytest.main()
