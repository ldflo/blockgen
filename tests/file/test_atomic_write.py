import blockgen
import pathlib
import tempfile

class Test:

    def test_1(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            was_created = blockgen.file.atomic_write(filepath, "Hello world!", encoding='utf-8', newline='\n')
            assert was_created is True
            with open(filepath, "r") as f:
                assert f.read() == "Hello world!"

            was_created = blockgen.file.atomic_write(filepath, "Hello world 2!")
            assert was_created is False
            with open(filepath, "r") as f:
                assert f.read() == "Hello world 2!"

            was_created = blockgen.file.atomic_write(filepath, "Hello world 2!")
            assert was_created is None # Unchanged
            with open(filepath, "r") as f:
                assert f.read() == "Hello world 2!"

    def test_2(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "dir1" / "dir2" / "file.txt"

            was_created = blockgen.file.atomic_write(filepath, "Hello world!", encoding='utf-8', newline='\n')
            assert was_created is True
            with open(filepath, "r") as f:
                assert f.read() == "Hello world!"

            was_created = blockgen.file.atomic_write(filepath, "Hello world 2!")
            assert was_created is False
            with open(filepath, "r") as f:
                assert f.read() == "Hello world 2!"

            was_created = blockgen.file.atomic_write(filepath, "Hello world 2!")
            assert was_created is None # Unchanged
            with open(filepath, "r") as f:
                assert f.read() == "Hello world 2!"
