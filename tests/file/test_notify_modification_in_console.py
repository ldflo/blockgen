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

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=None)
            assert stdout.getvalue() == f"[blockgen]  -------  {filepath}\n"

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=True)
            assert stdout.getvalue() == f"[blockgen]    new    {filepath}\n"

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=False)
            assert stdout.getvalue() == f"[blockgen]  changed  {filepath}\n"

class Test_Options:

    def test_1(self):
        try:
            os.environ["BLOCKGEN_SILENT"] = "0"
            with tempfile.TemporaryDirectory() as dir:
                filepath = pathlib.Path(dir) / "file.txt"

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.notify_modification_in_console(filepath, file_created=None)
                assert stdout.getvalue() == f"[blockgen]  -------  {filepath}\n"

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.notify_modification_in_console(filepath, file_created=True)
                assert stdout.getvalue() == f"[blockgen]    new    {filepath}\n"

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.notify_modification_in_console(filepath, file_created=False)
                assert stdout.getvalue() == f"[blockgen]  changed  {filepath}\n"
        finally:
            del os.environ["BLOCKGEN_SILENT"]

    def test_2(self):
        try:
            os.environ["BLOCKGEN_SILENT"] = "1"
            with tempfile.TemporaryDirectory() as dir:
                filepath = pathlib.Path(dir) / "file.txt"

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.notify_modification_in_console(filepath, file_created=None)
                assert len(stdout.getvalue()) == 0

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.notify_modification_in_console(filepath, file_created=True)
                assert len(stdout.getvalue()) == 0

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.notify_modification_in_console(filepath, file_created=False)
                assert len(stdout.getvalue()) == 0
        finally:
            del os.environ["BLOCKGEN_SILENT"]

    def test_3(self):
        try:
            blockgen.set_env_BLOCKGEN_SILENT(True)
            with tempfile.TemporaryDirectory() as dir:
                filepath = pathlib.Path(dir) / "file.txt"

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.notify_modification_in_console(filepath, file_created=None)
                assert len(stdout.getvalue()) == 0

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.notify_modification_in_console(filepath, file_created=True)
                assert len(stdout.getvalue()) == 0

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.notify_modification_in_console(filepath, file_created=False)
                assert len(stdout.getvalue()) == 0
        finally:
            blockgen.set_env_BLOCKGEN_SILENT(None)

    def test_4(self):
        with blockgen.options(silent=True):
            with tempfile.TemporaryDirectory() as dir:
                filepath = pathlib.Path(dir) / "file.txt"

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.notify_modification_in_console(filepath, file_created=None)
                assert len(stdout.getvalue()) == 0

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.notify_modification_in_console(filepath, file_created=True)
                assert len(stdout.getvalue()) == 0

                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    blockgen.file.notify_modification_in_console(filepath, file_created=False)
                assert len(stdout.getvalue()) == 0

    def test_5(self):
        try:
            os.environ["BLOCKGEN_NOTIFY_ABSOLUTE_PATH"] = "1"
            filepath = "./file.txt"

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=None)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]  -------  "):]) == True

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=True)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]    new    "):]) == True

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=False)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]  changed  "):]) == True
        finally:
            del os.environ["BLOCKGEN_NOTIFY_ABSOLUTE_PATH"]

    def test_6(self):
        try:
            blockgen.set_env_BLOCKGEN_NOTIFY_ABSOLUTE_PATH(True)
            filepath = "./file.txt"

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=None)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]  -------  "):]) == True

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=True)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]    new    "):]) == True

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=False)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]  changed  "):]) == True
        finally:
            blockgen.set_env_BLOCKGEN_NOTIFY_ABSOLUTE_PATH(None)

    def test_7(self):
        with blockgen.options(notify_absolute_path=True):
            filepath = "./file.txt"

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=None)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]  -------  "):]) == True

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=True)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]    new    "):]) == True

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=False)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]  changed  "):]) == True

    def test_8(self):
        try:
            os.environ["BLOCKGEN_NOTIFY_ABSOLUTE_PATH"] = "0"
            filepath = "./file.txt"

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=None)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]  -------  "):]) == False

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=True)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]    new    "):]) == False

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=False)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]  changed  "):]) == False
        finally:
            del os.environ["BLOCKGEN_NOTIFY_ABSOLUTE_PATH"]

    def test_9(self):
        try:
            blockgen.set_env_BLOCKGEN_NOTIFY_ABSOLUTE_PATH(False)
            filepath = "./file.txt"

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=None)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]  -------  "):]) == False

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=True)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]    new    "):]) == False

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=False)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]  changed  "):]) == False
        finally:
            blockgen.set_env_BLOCKGEN_NOTIFY_ABSOLUTE_PATH(None)

    def test_10(self):
        with blockgen.options(notify_absolute_path=False):
            filepath = "./file.txt"

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=None)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]  -------  "):]) == False

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=True)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]    new    "):]) == False

            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                blockgen.file.notify_modification_in_console(filepath, file_created=False)
            assert os.path.isabs(stdout.getvalue()[len("[blockgen]  changed  "):]) == False
