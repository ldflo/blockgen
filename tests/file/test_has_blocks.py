import blockgen
import os
import pathlib
import tempfile

class Test:

    def test_1(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
            """
            with open(filepath, "w") as f:
                f.write(text)

            assert blockgen.file.has_blocks(filepath) == True

    def test_2(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            text = """
                <<[ block1 ]>>
                \xc3
                <<[ end ]>>
            """
            with open(filepath, "w", encoding="utf_7") as f:
                f.write(text)

            assert blockgen.file.has_blocks(filepath, encoding="utf_7") == True

class Test_ErrorCases:

    def test_1(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            text = """
                <<[ block1 ]>>
                abc
            """
            with open(filepath, "w") as f:
                f.write(text)

            try:
                blockgen.file.has_blocks(filepath)
                assert True
            except blockgen.MissingBlockEndMarkerError as e:
                assert False
