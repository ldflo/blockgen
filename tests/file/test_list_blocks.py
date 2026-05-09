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

            blocks = blockgen.file.list_blocks(filepath)
            assert blocks[0].name == "block1"
            assert blocks[0].content == "abc"

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

            blocks = blockgen.file.list_blocks(filepath, encoding="utf_7")
            assert blocks[0].name == "block1"
            assert blocks[0].content == "\xc3"

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
                blockgen.file.list_blocks(filepath)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                elines = str(e).splitlines()
                assert len(elines) == 2
                assert elines[0] == f"File \"{os.path.abspath(os.path.expanduser(filepath))}\":"
                assert elines[1] == f"Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 2, column 17"
