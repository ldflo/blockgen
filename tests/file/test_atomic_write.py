import blockgen
import pathlib
import tempfile

class Test:

    def test_1(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            was_created = blockgen.file.atomic_write(filepath, "Hello world!", encoding="utf-8", newline='\n')
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

            was_created = blockgen.file.atomic_write(filepath, "Hello world!", encoding="utf-8", newline='\n')
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

    def test_3(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            text = """
                Hello world!
                This is a test.
            """

            was_created = blockgen.file.atomic_write(filepath, text, encoding="utf-8", newline="\r\n")
            assert was_created is True
            with open(filepath, "r") as f:
                assert f.read() == text
            with open(filepath, "r", newline="\r\n") as f:
                assert f.read() == text.replace("\n", "\r\n")

            was_created = blockgen.file.atomic_write(filepath, text)
            assert was_created is None # Unchanged
