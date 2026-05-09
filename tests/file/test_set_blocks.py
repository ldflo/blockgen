import blockgen
import contextlib
import io
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

            blocks = {"block1": "tuvw"}
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = blockgen.file.set_blocks(filepath, blocks)
            assert result == """
                <<[ block1 ]>>
                tuvw
                <<[ end ]>>
            """
            assert stdout.getvalue() == f"[blockgen]  changed  {filepath}\n"

            with open(filepath, "r") as f:
                new_text = f.read()
            assert new_text == """
                <<[ block1 ]>>
                tuvw
                <<[ end ]>>
            """

    def test_2(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
            """
            with open(filepath, "w", encoding="utf_7") as f:
                f.write(text)

            blocks = {"block1": "\xc3"}
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = blockgen.file.set_blocks(filepath, blocks, encoding="utf_7")
            assert result == """
                <<[ block1 ]>>
                \xc3
                <<[ end ]>>
            """
            assert stdout.getvalue() == f"[blockgen]  changed  {filepath}\n"

            with open(filepath, "r", encoding="utf_7") as f:
                new_text = f.read()
            assert new_text == """
                <<[ block1 ]>>
                \xc3
                <<[ end ]>>
            """

    def test_3(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
            """
            with open(filepath, "w") as f:
                f.write(text)

            blocks = {"block1": "tuvw"}
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = blockgen.file.set_blocks(filepath, blocks, newline="\r\n")
            assert result == """
                <<[ block1 ]>>
                tuvw
                <<[ end ]>>
            """
            assert stdout.getvalue() == f"[blockgen]  changed  {filepath}\n"

            with open(filepath, "r", newline="\r\n") as f:
                new_text = f.read()
            assert new_text == """
                <<[ block1 ]>>
                tuvw
                <<[ end ]>>
            """.replace("\n", "\r\n")

    def test_4(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
            """
            with open(filepath, "w") as f:
                f.write(text)

            blocks = {"block1": lambda: blockgen.current_filepath.name}
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = blockgen.file.set_blocks(filepath, blocks)
            assert result == """
                <<[ block1 ]>>
                file.txt
                <<[ end ]>>
            """
            assert stdout.getvalue() == f"[blockgen]  changed  {filepath}\n"

            with open(filepath, "r") as f:
                new_text = f.read()
            assert new_text == """
                <<[ block1 ]>>
                file.txt
                <<[ end ]>>
            """

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
                blocks = {"block1": "tuvw"}
                blockgen.file.set_blocks(filepath, blocks)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                elines = str(e).splitlines()
                assert len(elines) == 2
                assert elines[0] == f"File \"{os.path.abspath(os.path.expanduser(filepath))}\":"
                assert elines[1] == f"Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 2, column 17"

class Test_Options:

    def test_1(self):
        try:
            os.environ["BLOCKGEN_SILENT"] = "1"
            with tempfile.TemporaryDirectory() as dir:
                filepath = pathlib.Path(dir) / "file.txt"

                text = """
                    <<[ block1 ]>>
                    abc
                    <<[ end ]>>
                """
                with open(filepath, "w") as f:
                    f.write(text)

                blocks = {"block1": "tuvw"}
                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.set_blocks(filepath, blocks)
                assert len(stdout.getvalue()) == 0
        finally:
            del os.environ["BLOCKGEN_SILENT"]

    def test_2(self):
        try:
            blockgen.set_env_BLOCKGEN_SILENT(True)
            with tempfile.TemporaryDirectory() as dir:
                filepath = pathlib.Path(dir) / "file.txt"

                text = """
                    <<[ block1 ]>>
                    abc
                    <<[ end ]>>
                """
                with open(filepath, "w") as f:
                    f.write(text)

                blocks = {"block1": "tuvw"}
                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.set_blocks(filepath, blocks)
                assert len(stdout.getvalue()) == 0
        finally:
            blockgen.set_env_BLOCKGEN_SILENT(None)

    def test_3(self):
        with blockgen.options(silent=True):
            with tempfile.TemporaryDirectory() as dir:
                filepath = pathlib.Path(dir) / "file.txt"

                text = """
                    <<[ block1 ]>>
                    abc
                    <<[ end ]>>
                """
                with open(filepath, "w") as f:
                    f.write(text)

                blocks = {"block1": "tuvw"}
                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.set_blocks(filepath, blocks)
                assert len(stdout.getvalue()) == 0
