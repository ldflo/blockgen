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

            new_text = """
                <<[ block1 ]>>
                tuvw
                <<[ end ]>>
                <<[ block2 ]>>
                xyz
                <<[ end ]>>
            """
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = blockgen.file.write_and_reinject_blocks(filepath, new_text)
            assert result == """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
                <<[ block2 ]>>
                xyz
                <<[ end ]>>
            """
            assert stdout.getvalue() == f"[blockgen]  changed  {filepath}\n"

            with open(filepath, "r") as f:
                new_text = f.read()
            assert new_text == """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
                <<[ block2 ]>>
                xyz
                <<[ end ]>>
            """

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

            new_text = """
                <<[ block1 ]>>
                tuvw
                <<[ end ]>>
                <<[ block2 ]>>
                \xc3
                <<[ end ]>>
            """
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = blockgen.file.write_and_reinject_blocks(filepath, new_text, encoding="utf_7")
            assert result == """
                <<[ block1 ]>>
                \xc3
                <<[ end ]>>
                <<[ block2 ]>>
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
                <<[ block2 ]>>
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

            new_text = """
                <<[ block1 ]>>
                \xc3
                <<[ end ]>>
                <<[ block2 ]>>
                \xc3
                <<[ end ]>>
            """
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = blockgen.file.write_and_reinject_blocks(filepath, new_text, newline="\r\n")
            assert result == """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
                <<[ block2 ]>>
                \xc3
                <<[ end ]>>
            """
            assert stdout.getvalue() == f"[blockgen]  changed  {filepath}\n"

            with open(filepath, "r", newline="\r\n") as f:
                new_text = f.read()
            assert new_text == """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
                <<[ block2 ]>>
                \xc3
                <<[ end ]>>
            """.replace("\n", "\r\n")

    def test_4(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            new_text = """
                <<[ block1 ]>>
                \xc3
                <<[ end ]>>
                <<[ block2 ]>>
                \xc3
                <<[ end ]>>
            """
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = blockgen.file.write_and_reinject_blocks(filepath, new_text)
            assert result == """
                <<[ block1 ]>>
                \xc3
                <<[ end ]>>
                <<[ block2 ]>>
                \xc3
                <<[ end ]>>
            """
            assert stdout.getvalue() == f"[blockgen]    new    {filepath}\n"

            with open(filepath, "r") as f:
                new_text = f.read()
            assert new_text == """
                <<[ block1 ]>>
                \xc3
                <<[ end ]>>
                <<[ block2 ]>>
                \xc3
                <<[ end ]>>
            """

class Test_ErrorCases:

    def test_1(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
                <<[ block2 ]>>
                def
                <<[ end ]>>
            """
            with open(filepath, "w") as f:
                f.write(text)

            new_text = """
                <<[ block1 ]>>
                tuvw
                <<[ end ]>>
            """
            try:
                blockgen.file.write_and_reinject_blocks(filepath, new_text)
                assert False
            except blockgen.NonReinjectedBlockError as e:
                elines = str(e).splitlines()
                assert len(elines) == 2
                assert elines[0] == f"File \"{os.path.abspath(os.path.expanduser(filepath))}\":"
                assert elines[1] == f"Destination block not found, couldn't reinject block '<<[ block2 ]>>' at line 5, column 17"
            except Exception:
                raise

    def test_2(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            text = """
                <<[ block1(1, 2, 3) ]>>
                abc
                <<[ end ]>>
            """
            with open(filepath, "w") as f:
                f.write(text)

            new_text = """
                <<[ block1 ]>>
                tuvw
                <<[ end ]>>
            """
            try:
                blockgen.file.write_and_reinject_blocks(filepath, new_text)
                assert False
            except blockgen.NonReinjectedBlockError as e:
                elines = str(e).splitlines()
                assert len(elines) == 2
                assert elines[0] == f"File \"{os.path.abspath(os.path.expanduser(filepath))}\":"
                assert elines[1] == f"Destination block not found, couldn't reinject block '<<[ block1(1, 2, 3) ]>>' at line 2, column 17"
            except Exception:
                raise

    def test_3(self):
        with tempfile.TemporaryDirectory() as dir:
            filepath = pathlib.Path(dir) / "file.txt"

            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
                <<[ block2 ]>>
                def
                <<[ end ]>>
            """
            with open(filepath, "w") as f:
                f.write(text)

            new_text = """
                <<[ block3 ]>>
                tuvw
                <<[ end ]>>
            """
            try:
                blockgen.file.write_and_reinject_blocks(filepath, new_text)
                assert False
            except blockgen.NonReinjectedBlockError as e:
                elines = str(e).splitlines()
                assert len(elines) == 4
                assert elines[0] == f"File \"{os.path.abspath(os.path.expanduser(filepath))}\":"
                assert elines[1] == f"Destination blocks not found, couldn't reinject the following blocks:"
                assert elines[2] == f"    '<<[ block1 ]>>' at line 2, column 17"
                assert elines[3] == f"    '<<[ block2 ]>>' at line 5, column 17"
            except Exception:
                raise

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

                new_text = """
                    <<[ block1 ]>>
                    tuvw
                    <<[ end ]>>
                    <<[ block2 ]>>
                    xyz
                    <<[ end ]>>
                """
                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.write_and_reinject_blocks(filepath, new_text)
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

                new_text = """
                    <<[ block1 ]>>
                    tuvw
                    <<[ end ]>>
                    <<[ block2 ]>>
                    xyz
                    <<[ end ]>>
                """
                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.write_and_reinject_blocks(filepath, new_text)
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

                new_text = """
                    <<[ block1 ]>>
                    tuvw
                    <<[ end ]>>
                    <<[ block2 ]>>
                    xyz
                    <<[ end ]>>
                """
                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.write_and_reinject_blocks(filepath, new_text)
                assert len(stdout.getvalue()) == 0

    def test_4(self):
        try:
            os.environ["BLOCKGEN_DISABLE_SAFEGUARD"] = "1"
            with tempfile.TemporaryDirectory() as dir:
                filepath = pathlib.Path(dir) / "file.txt"

                text = """
                    <<[ block1 ]>>
                    abc
                    <<[ end ]>>
                """
                with open(filepath, "w") as f:
                    f.write(text)

                new_text = """
                    <<[ block2 ]>>
                    xyz
                    <<[ end ]>>
                """
                result = blockgen.file.write_and_reinject_blocks(filepath, new_text)
                assert result == new_text
        finally:
            del os.environ["BLOCKGEN_DISABLE_SAFEGUARD"]

    def test_5(self):
        try:
            blockgen.set_env_BLOCKGEN_DISABLE_SAFEGUARD(True)
            with tempfile.TemporaryDirectory() as dir:
                filepath = pathlib.Path(dir) / "file.txt"

                text = """
                    <<[ block1 ]>>
                    abc
                    <<[ end ]>>
                """
                with open(filepath, "w") as f:
                    f.write(text)

                new_text = """
                    <<[ block2 ]>>
                    xyz
                    <<[ end ]>>
                """
                result = blockgen.file.write_and_reinject_blocks(filepath, new_text)
                assert result == new_text
        finally:
            blockgen.set_env_BLOCKGEN_DISABLE_SAFEGUARD(None)

    def test_6(self):
        with blockgen.options(disable_safeguard=True):
            with tempfile.TemporaryDirectory() as dir:
                filepath = pathlib.Path(dir) / "file.txt"

                text = """
                    <<[ block1 ]>>
                    abc
                    <<[ end ]>>
                """
                with open(filepath, "w") as f:
                    f.write(text)

                new_text = """
                    <<[ block2 ]>>
                    xyz
                    <<[ end ]>>
                """
                result = blockgen.file.write_and_reinject_blocks(filepath, new_text)
                assert result == new_text
