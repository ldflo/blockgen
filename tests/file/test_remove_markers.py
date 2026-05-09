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

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = blockgen.file.remove_markers(filepath)
            assert result == """
                abc
            """
            assert stdout.getvalue() == f"[blockgen]  changed  {filepath}\n"

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

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = blockgen.file.remove_markers(filepath, encoding="utf_7")
            assert result == """
                \xc3
            """
            assert stdout.getvalue() == f"[blockgen]  changed  {filepath}\n"

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

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = blockgen.file.remove_markers(filepath, newline="\r\n")
            assert result == """
                abc
            """
            assert stdout.getvalue() == f"[blockgen]  changed  {filepath}\n"

            with open(filepath, "r", newline="\r\n") as f:
                new_text = f.read()
            assert new_text == """
                abc
            """.replace("\n", "\r\n")

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
                blockgen.file.remove_markers(filepath)
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

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.remove_markers(filepath)
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

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.remove_markers(filepath)
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

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.remove_markers(filepath)
                assert len(stdout.getvalue()) == 0
