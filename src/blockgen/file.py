import os
import pathlib
import stat
import tempfile
from types import FunctionType
from typing import Generator, Optional, Type, Union

from . import core
from . import string

def has_blocks(
    file: Union[str, os.PathLike],
    *,
    encoding: Optional[str] = None,
) -> bool:
    """ Checks whether the given file contains at least one block marker.

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file to search for block markers.
        encoding: Optional[str]
            The encoding used when reading the file.

        Returns
        -------
        bool
            `True` if at least one block marker is found, `False` otherwise.

        Raises
        ------
        BaseException
            All exceptions raised by `open()` built-in function.

        Notes
        -----
        By default, a block marker is of the form `<<[ block_expression ]>>`.

        You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["` and `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`
        or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>')`.
    """
    with open(file, "r", encoding=encoding) as f:
        text = f.read()
    return string.has_blocks(text)

def parse_blocks(
    file: Union[str, os.PathLike],
    *,
    encoding: Optional[str] = None,
) -> Generator[core.Block, None, None]:
    """ Parses all blocks found in the given file, yielding them one by one.

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file to parse for blocks.
        encoding: Optional[str]
            The encoding used when reading the file.

        Yields
        ------
        blockgen.Block
            Each block found in the file, in order of appearance.

        Raises
        ------
        BaseException
            All exceptions raised by `open()` built-in function.
        blockgen.MissingBlockEndMarkerError
            If an opening block marker has no matching ending block marker.
        blockgen.UnmatchedBlockEndMarkerError
            If an ending block marker is found without a preceding opening block marker.
        blockgen.MissingSpacesBetweenBlockMarkersError
            If there are no spaces between block markers.
        blockgen.NamelessBlockError
            If an opening block marker has an empty block expression.
        blockgen.BlockExpressionError
            If a block expression is invalid.
        blockgen.DuplicatedBlockExpressionError
            If two blocks share the same (supposedly unique) expression.

        Notes
        -----
        By default, a block is of the form `<<[ block_expression ]>> block_content <<[ end ]>>`.

        You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["`, `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`, and `BLOCKGEN_END_BLOCK_EXPRESSION="end"`
        or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>', end_block_expression='end')`.
    """
    with open(file, "r", encoding=encoding) as f:
        text = f.read()
    def defer():
        try:
            yield from string.parse_blocks(text)
        except core.BaseException as e:
            e.args = (f"File \"{os.path.abspath(os.path.expanduser(file))}\":\n" + e.args[0],) + e.args[1:]
            raise
    return defer()

def list_blocks(
    file: Union[str, os.PathLike],
    *,
    encoding: Optional[str] = None,
) -> list[core.Block]:
    """ Returns the list of all blocks found in the given file.

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file to parse for blocks.
        encoding: Optional[str]
            The encoding used when reading the file.

        Returns
        -------
        list[blockgen.Block]
            A list of all blocks found in the file, in order of appearance.

        Raises
        ------
        BaseException
            All exceptions raised by `open()` built-in function.
        blockgen.MissingBlockEndMarkerError
            If an opening block marker has no matching ending block marker.
        blockgen.UnmatchedBlockEndMarkerError
            If an ending block marker is found without a preceding opening block marker.
        blockgen.MissingSpacesBetweenBlockMarkersError
            If there are no spaces between block markers.
        blockgen.NamelessBlockError
            If an opening block marker has an empty block expression.
        blockgen.BlockExpressionError
            If a block expression is invalid.
        blockgen.DuplicatedBlockExpressionError
            If two blocks share the same (supposedly unique) expression.

        Notes
        -----
        By default, a block is of the form `<<[ block_expression ]>> block_content <<[ end ]>>`.

        You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["`, `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`, and `BLOCKGEN_END_BLOCK_EXPRESSION="end"`
        or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>', end_block_expression='end')`.
    """
    try:
        with open(file, "r", encoding=encoding) as f:
            text = f.read()
        return string.list_blocks(text)
    except core.BaseException as e:
        e.args = (f"File \"{os.path.abspath(os.path.expanduser(file))}\":\n" + e.args[0],) + e.args[1:]
        raise

def get_blocks(
    file: Union[str, os.PathLike],
    *,
    encoding: Optional[str] = None,
) -> dict[str, str]:
    """ Returns a dictionary of all blocks found in the given file.

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file to parse for blocks.
        encoding: Optional[str]
            The encoding used when reading the file.

        Returns
        -------
        dict[str, str]
            A dictionary mapping each block expression to its content, in order of appearance.

        Raises
        ------
        BaseException
            All exceptions raised by `open()` built-in function.
        blockgen.MissingBlockEndMarkerError
            If an opening block marker has no matching ending block marker.
        blockgen.UnmatchedBlockEndMarkerError
            If an ending block marker is found without a preceding opening block marker.
        blockgen.MissingSpacesBetweenBlockMarkersError
            If there are no spaces between block markers.
        blockgen.NamelessBlockError
            If an opening block marker has an empty block expression.
        blockgen.BlockExpressionError
            If a block expression is invalid.
        blockgen.DuplicatedBlockExpressionError
            If two blocks share the same (supposedly unique) expression.

        Notes
        -----
        By default, a block is of the form `<<[ block_expression ]>> block_content <<[ end ]>>`.

        You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["`, `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`, and `BLOCKGEN_END_BLOCK_EXPRESSION="end"`
        or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>', end_block_expression='end')`.
    """
    try:
        with open(file, "r", encoding=encoding) as f:
            text = f.read()
        return string.get_blocks(text)
    except core.BaseException as e:
        e.args = (f"File \"{os.path.abspath(os.path.expanduser(file))}\":\n" + e.args[0],) + e.args[1:]
        raise

def set_blocks(
    file: Union[str, os.PathLike],
    blocks: dict[str, Union[str, FunctionType, object, Type, None]],
    *,
    encoding: Optional[str] = None,
    newline: Optional[str] = None,
) -> str:
    """ Sets the content of the specified blocks in the given file.
        If the file content is the same, the file is left unchanged to avoid unnecessary file modification.

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file containing the blocks to update.
        blocks: dict[str, Union[str, FunctionType, object, Type, None]]
            A dictionary mapping block expressions to their new content.

            The given keys can be:
            - A block name, e.g. `"block1"`
            - A full parameterized block expression, e.g. `"block1('a', 1, param=[1, 2, 3])"`
            - The `"*"` to match all remaining blocks not matched by a more specific key

            For block names or the `"*"` wildcard, values can be:
            - `None`: leaves the block content unchanged
            - A `str`: used directly as the new block content
            - A function `(*args, **kwargs) -> Optional[str]`: return value used as the new block content
            - A class instance with `@blockgen.callback("block_name")` decorated methods `(self, *args, **kwargs) -> Optional[str]`: return value used as the new block content
            - A class type with `@blockgen.callback("block_name")` decorated static methods `(*args, **kwargs) -> Optional[str]`: return value used as the new block content

            For full parameterized block expressions, values can be:
            - `None`: leaves the block content unchanged
            - A `str`: used directly as the new block content
        encoding: Optional[str]
            The encoding used when reading and writing the file.
        newline: Optional[str]
            The newline character(s) used when writing the file.

        Returns
        -------
        str
            The new file content with the specified block contents replaced.

        Raises
        ------
        BaseException
            All exceptions raised by `open()` built-in function.
        blockgen.MissingBlockEndMarkerError
            If an opening block marker has no matching ending block marker.
        blockgen.UnmatchedBlockEndMarkerError
            If an ending block marker is found without a preceding opening block marker.
        blockgen.MissingSpacesBetweenBlockMarkersError
            If there are no spaces between block markers.
        blockgen.NamelessBlockError
            If an opening block marker has an empty block expression.
        blockgen.BlockExpressionError
            If a block expression is invalid.
        blockgen.DuplicatedBlockExpressionError
            If two blocks share the same (supposedly unique) expression.
        blockgen.CallbackDecoratorBlockNameError
            If a block name used in a callback decorator is invalid.
        blockgen.DuplicatedCallbackDecoratorBlockNameError
            If two callback decorators share the same block name.
        blockgen.InvalidValueTypeError
            If a value given in the `blocks` dictionary is not of an allowed type.
        blockgen.BlockCallbackError
            If an error occurs when replacing a block content with a callback.
        blockgen.CallbackNotFoundError
            If a generic callback for replacing a block content is not found.
        blockgen.BlockContentError
            If a block content contains newlines but the block is inline.

        Notes
        -----
        Use `blockgen.current_block` to access the current `blockgen.Block` object from within callbacks.
        Use `blockgen.current_filepath` to access the current filepath from within callbacks.

        By default, a block is of the form `<<[ block_expression ]>> block_content <<[ end ]>>`.

        You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["`, `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`, and `BLOCKGEN_END_BLOCK_EXPRESSION="end"`
        or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>', end_block_expression='end')`.

        After writing the file, a notification is printed to the console indicating that the file was created, changed, or left unchanged:
        ```
        $ [blockgen]    new    /absolute/path/to/file
        $ [blockgen]  changed  /absolute/path/to/file
        $ [blockgen]  -------  /absolute/path/to/file
        ```

        You can also choose to print relative paths in these notifications with the environment variable `BLOCKGEN_NOTIFY_ABSOLUTE_PATH="0"`
        or with `blockgen.options(notify_absolute_path=False)`:
        ```
        $ [blockgen]    new    ./relative/path/to/file
        $ [blockgen]  changed  ./relative/path/to/file
        $ [blockgen]  -------  ./relative/path/to/file
        ```

        You can disable these notifications with the environment variable `BLOCKGEN_SILENT="1"`
        or with `blockgen.options(silent=True)`.

        Examples
        --------
        ```
        class InstanceClass:
            @blockgen.callback("block3")
            def callback(self, *args, **kwargs) -> Optional[str]:
                return f"new content inside {blockgen.current_filepath}"

            @blockgen.callback("*")
            def generic_callback(self, *args, **kwargs) -> Optional[str]:
                return f"new content for {blockgen.current_block.name}"

        class StaticClass:
            @staticmethod
            @blockgen.callback("block3")
            def callback(*args, **kwargs) -> Optional[str]:
                return f"new content inside {blockgen.current_filepath}"

            @staticmethod
            @blockgen.callback("*")
            def generic_callback(*args, **kwargs) -> Optional[str]:
                return f"new content for {blockgen.current_block.name}"

        blocks = {
            "block1('a', 1, param=[1, 2, 3])": "new content",
            "block2": lambda *args, **kwargs: f"new content inside {blockgen.current_filepath}",
            "*": InstanceClass(),
            # Alternatively
            # "*": StaticClass,
        }
        new_text = blockgen.file.set_blocks("/path/to/file.txt", blocks)
        ```
    """
    try:
        with open(file, "r", encoding=encoding) as f:
            text = f.read()
        with core.context(filepath=file):
            new_text = string.set_blocks(text, blocks)
        atomic_write(file, new_text, encoding=encoding, newline=newline)
        return new_text
    except core.BaseException as e:
        e.args = (f"File \"{os.path.abspath(os.path.expanduser(file))}\":\n" + e.args[0],) + e.args[1:]
        raise

def replace_blocks(
    file: Union[str, os.PathLike],
    blocks: dict[str, Union[str, None]],
    *,
    encoding: Optional[str] = None,
    newline: Optional[str] = None,
) -> str:
    """ Replaces the content of the specified blocks in the given file.
        If the file content is the same, the file is left unchanged to avoid unnecessary file modification.
        Uses a safeguard that raises an error if any of the specified blocks is not found in the file.

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file containing the blocks to update.
        blocks: dict[str, Union[str, None]]
            A dictionary mapping block expressions to their new content.

            The given keys must be the same exact block expressions of the blocks in the file.

            The value `None` leaves the block content unchanged.
        encoding: Optional[str]
            The encoding used when reading and writing the file.
        newline: Optional[str]
            The newline character(s) used when writing the file.

        Returns
        -------
        str
            The new file content with the specified block contents replaced.

        Raises
        ------
        BaseException
            All exceptions raised by `open()` built-in function.
        blockgen.MissingBlockEndMarkerError
            If an opening block marker has no matching ending block marker.
        blockgen.UnmatchedBlockEndMarkerError
            If an ending block marker is found without a preceding opening block marker.
        blockgen.MissingSpacesBetweenBlockMarkersError
            If there are no spaces between block markers.
        blockgen.NamelessBlockError
            If an opening block marker has an empty block expression.
        blockgen.BlockExpressionError
            If a block expression is invalid.
        blockgen.DuplicatedBlockExpressionError
            If two blocks share the same (supposedly unique) expression.
        blockgen.BlockContentError
            If a block content contains newlines but the block is inline.
        blockgen.NonReplacedBlockError
            If at least one of the specified blocks is not found in the file.

        Notes
        -----
        By default, a block is of the form `<<[ block_expression ]>> block_content <<[ end ]>>`.

        You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["`, `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`, and `BLOCKGEN_END_BLOCK_EXPRESSION="end"`
        or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>', end_block_expression='end')`.

        You can disable the safeguard with the environment variable `BLOCKGEN_DISABLE_SAFEGUARD="1"`
        or with `blockgen.options(disable_safeguard=True)`.

        After writing the file, a notification is printed to the console indicating that the file was created, changed, or left unchanged:
        ```
        $ [blockgen]    new    /absolute/path/to/file
        $ [blockgen]  changed  /absolute/path/to/file
        $ [blockgen]  -------  /absolute/path/to/file
        ```

        You can also choose to print relative paths in these notifications with the environment variable `BLOCKGEN_NOTIFY_ABSOLUTE_PATH="0"`
        or with `blockgen.options(notify_absolute_path=False)`:
        ```
        $ [blockgen]    new    ./relative/path/to/file
        $ [blockgen]  changed  ./relative/path/to/file
        $ [blockgen]  -------  ./relative/path/to/file
        ```

        You can disable these notifications with the environment variable `BLOCKGEN_SILENT="1"`
        or with `blockgen.options(silent=True)`.
    """
    try:
        with open(file, "r", encoding=encoding) as f:
            text = f.read()
        new_text = string.replace_blocks(text, blocks)
        atomic_write(file, new_text, encoding=encoding, newline=newline)
        return new_text
    except core.BaseException as e:
        e.args = (f"File \"{os.path.abspath(os.path.expanduser(file))}\":\n" + e.args[0],) + e.args[1:]
        raise

def remove_markers(
    file: Union[str, os.PathLike],
    *,
    encoding: Optional[str] = None,
    newline: Optional[str] = None,
) -> str:
    """ Removes all block markers from the given file, keeping only the block contents.
        If the file content is the same, the file is left unchanged to avoid unnecessary file modification.

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file containing the block markers to remove.
        encoding: Optional[str]
            The encoding used when reading and writing the file.
        newline: Optional[str]
            The newline character(s) used when writing the file.

        Returns
        -------
        str
            The new file content with all block markers removed and only the block contents retained.

        Raises
        ------
        BaseException
            All exceptions raised by `open()` built-in function.
        blockgen.MissingBlockEndMarkerError
            If an opening block marker has no matching ending block marker.
        blockgen.UnmatchedBlockEndMarkerError
            If an ending block marker is found without a preceding opening block marker.
        blockgen.MissingSpacesBetweenBlockMarkersError
            If there are no spaces between block markers.
        blockgen.NamelessBlockError
            If an opening block marker has an empty block expression.
        blockgen.BlockExpressionError
            If a block expression is invalid.
        blockgen.DuplicatedBlockExpressionError
            If two blocks share the same (supposedly unique) expression.

        Notes
        -----
        By default, a block is of the form `<<[ block_expression ]>> block_content <<[ end ]>>`.

        You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["`, `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`, and `BLOCKGEN_END_BLOCK_EXPRESSION="end"`
        or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>', end_block_expression='end')`.

        After writing the file, a notification is printed to the console indicating that the file was created, changed, or left unchanged:
        ```
        $ [blockgen]    new    /absolute/path/to/file
        $ [blockgen]  changed  /absolute/path/to/file
        $ [blockgen]  -------  /absolute/path/to/file
        ```

        You can also choose to print relative paths in these notifications with the environment variable `BLOCKGEN_NOTIFY_ABSOLUTE_PATH="0"`
        or with `blockgen.options(notify_absolute_path=False)`:
        ```
        $ [blockgen]    new    ./relative/path/to/file
        $ [blockgen]  changed  ./relative/path/to/file
        $ [blockgen]  -------  ./relative/path/to/file
        ```

        You can disable these notifications with the environment variable `BLOCKGEN_SILENT="1"`
        or with `blockgen.options(silent=True)`.
    """
    try:
        with open(file, "r", encoding=encoding) as f:
            text = f.read()
        new_text = string.remove_markers(text)
        atomic_write(file, new_text, encoding=encoding, newline=newline)
        return new_text
    except core.BaseException as e:
        e.args = (f"File \"{os.path.abspath(os.path.expanduser(file))}\":\n" + e.args[0],) + e.args[1:]
        raise

def write_and_reinject_blocks(
    file: Union[str, os.PathLike],
    text: str,
    *,
    encoding: Optional[str] = None,
    newline: Optional[str] = None,
    mkdir: bool = True,
) -> str:
    """ Writes the given text to the file and reinjects the old block contents from the file into the new text.
        If the file does not exist yet, the text is written as-is.
        If the file content is the same, the file is left unchanged to avoid unnecessary file modification.
        Uses a safeguard that raises an error if any old block from the existing file cannot be reinjected in the new text.

        Equivalent to:
        ```
        old_blocks = blockgen.file.get_blocks(file)
        with open(file, "w") as f:
            f.write(text)
        blockgen.file.replace_blocks(file, old_blocks)
        ```

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file to write to and reinject blocks into.
        text: str
            The text to write to the file.
        encoding: Optional[str]
            The encoding used when reading and writing the file.
        newline: Optional[str]
            The newline character(s) used when writing the file.
        mkdir: bool
            If `True` (default), creates parent directories of the file if they do not exist.

        Returns
        -------
        str
            The written text, with the old block contents reinjected.

        Raises
        ------
        BaseException
            All exceptions raised by `open()` built-in function.
        blockgen.MissingBlockEndMarkerError
            If an opening block marker has no matching ending block marker.
        blockgen.UnmatchedBlockEndMarkerError
            If an ending block marker is found without a preceding opening block marker.
        blockgen.MissingSpacesBetweenBlockMarkersError
            If there are no spaces between block markers.
        blockgen.NamelessBlockError
            If an opening block marker has an empty block expression.
        blockgen.BlockExpressionError
            If a block expression is invalid.
        blockgen.DuplicatedBlockExpressionError
            If two blocks share the same (supposedly unique) expression.
        blockgen.BlockContentError
            If a block content contains newlines but the block is inline.
        blockgen.NonReinjectedBlockError
            If at least one block from the existing file cannot be reinjected in the new text.

        Notes
        -----
        By default, a block is of the form `<<[ block_expression ]>> block_content <<[ end ]>>`.

        You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["`, `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`, and `BLOCKGEN_END_BLOCK_EXPRESSION="end"`
        or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>', end_block_expression='end')`.

        You can disable the safeguard with the environment variable `BLOCKGEN_DISABLE_SAFEGUARD="1"`
        or with `blockgen.options(disable_safeguard=True)`.

        After writing the file, a notification is printed to the console indicating that the file was created, changed, or left unchanged:
        ```
        $ [blockgen]    new    /absolute/path/to/file
        $ [blockgen]  changed  /absolute/path/to/file
        $ [blockgen]  -------  /absolute/path/to/file
        ```

        You can also choose to print relative paths in these notifications with the environment variable `BLOCKGEN_NOTIFY_ABSOLUTE_PATH="0"`
        or with `blockgen.options(notify_absolute_path=False)`:
        ```
        $ [blockgen]    new    ./relative/path/to/file
        $ [blockgen]  changed  ./relative/path/to/file
        $ [blockgen]  -------  ./relative/path/to/file
        ```

        You can disable these notifications with the environment variable `BLOCKGEN_SILENT="1"`
        or with `blockgen.options(silent=True)`.
    """
    cfg = core.BLOCKGEN_OPTIONS.get()

    try:
        if os.path.isfile(file):
            with open(file, "r", encoding=encoding) as f:
                old_text = f.read()
            old_blocks = string.list_blocks(old_text)

            # Verify that all old blocks can be reinjected in the new text
            if not cfg.get_disable_safeguard():
                new_blocks = string.list_blocks(text)
                missing_blocks: list[core.Block] = []
                for old_block in old_blocks:
                    found = False
                    for new_block in new_blocks:
                        if new_block.expression == old_block.expression:
                            found = True
                            break
                    if not found:
                        missing_blocks.append(old_block)
                if len(missing_blocks) > 0:
                    raise core._exception_non_reinjected_block(missing_blocks)

            text = string.set_blocks(text, {old_block.expression: old_block.content for old_block in old_blocks})
        atomic_write(file, text, encoding=encoding, newline=newline, mkdir=mkdir)
        return text
    except core.BaseException as e:
        e.args = (f"File \"{os.path.abspath(os.path.expanduser(file))}\":\n" + e.args[0],) + e.args[1:]
        raise

def atomic_write(
    file: Union[str, os.PathLike],
    text: str,
    *,
    encoding: Optional[str] = None,
    newline: Optional[str] = None,
    mkdir: bool = True,
) -> Optional[bool]:
    """ Writes the given text to the file atomically.
        If the file content is the same, the file is left unchanged to avoid unnecessary file modification.

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file to write to.
        text: str
            The text to write to the file.
        encoding: Optional[str]
            The encoding used when reading and writing the file.
        newline: Optional[str]
            The newline character(s) used when writing the file.
        mkdir: bool
            If `True` (default), creates parent directories of the file if they do not exist.

        Returns
        -------
        Optional[bool]
            - `True` if the file was created
            - `False` if the file was modified
            - `None` if the file was left unchanged

        Raises
        ------
        BaseException
            All exceptions raised by `open()` built-in function.

        Notes
        -----
        After writing the file, a notification is printed to the console indicating that the file was created, changed, or left unchanged:
        ```
        $ [blockgen]    new    /absolute/path/to/file
        $ [blockgen]  changed  /absolute/path/to/file
        $ [blockgen]  -------  /absolute/path/to/file
        ```

        You can also choose to print relative paths in these notifications with the environment variable `BLOCKGEN_NOTIFY_ABSOLUTE_PATH="0"`
        or with `blockgen.options(notify_absolute_path=False)`:
        ```
        $ [blockgen]    new    ./relative/path/to/file
        $ [blockgen]  changed  ./relative/path/to/file
        $ [blockgen]  -------  ./relative/path/to/file
        ```

        You can disable these notifications with the environment variable `BLOCKGEN_SILENT="1"`
        or with `blockgen.options(silent=True)`.
    """
    filepath = pathlib.Path(file)

    # Only rewrite file if content has changed
    st = None
    try:
        st = filepath.stat()
        with filepath.open("r", encoding=encoding) as f:
            if f.read() == text:
                notify_modification_in_console(file, file_created=None)
                return None # No file modification (mtime unchanged)
    except FileNotFoundError:
        pass

    # Create parent directories if needed
    if mkdir:
        filepath.parent.mkdir(parents=True, exist_ok=True)

    # Write to temporary file and atomically rename
    fd, tmp = tempfile.mkstemp(prefix=filepath.name + ".", dir=filepath.parent)
    try:
        with os.fdopen(fd, "w", encoding=encoding, newline=newline) as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        # Preserve file chmod
        if st is not None:
            os.chmod(tmp, stat.S_IMODE(st.st_mode))
        # Atomic replace
        os.replace(tmp, filepath)
    finally:
        # Cleanup temporary file
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass

    file_created = st is None # True if file created, False if file modified
    notify_modification_in_console(file, file_created=file_created)
    return file_created

def notify_modification_in_console(
    file: Union[str, os.PathLike],
    *,
    file_created: Optional[bool]):
    """ Prints a notification to the console indicating whether the file was created, modified, or left unchanged.

        Parameters
        ----------
        file: Union[str, os.PathLike]
            The file that was written to.
        file_created: Optional[bool]
            - `True` if the file was created
            - `False` if the file was modified
            - `None` if the file was left unchanged

        Notes
        -----
        The notification is printed in one of the following formats:
        ```
        $ [blockgen]    new    /absolute/path/to/file
        $ [blockgen]  changed  /absolute/path/to/file
        $ [blockgen]  -------  /absolute/path/to/file
        ```

        You can also choose to print relative paths in these notifications with the environment variable `BLOCKGEN_NOTIFY_ABSOLUTE_PATH="0"`
        or with `blockgen.options(notify_absolute_path=False)`:
        ```
        $ [blockgen]    new    ./relative/path/to/file
        $ [blockgen]  changed  ./relative/path/to/file
        $ [blockgen]  -------  ./relative/path/to/file
        ```

        You can disable these notifications with the environment variable `BLOCKGEN_SILENT="1"`
        or with `blockgen.options(silent=True)`.
    """
    cfg = core.BLOCKGEN_OPTIONS.get()

    if cfg.get_silent() is True:
        return # Do not print any notification if silent mode is enabled

    if cfg.get_notify_absolute_path():
        file = os.path.abspath(os.path.expanduser(file))

    if file_created is None:
        result = f"[blockgen]  -------  {file}"
    elif file_created:
        result = f"[blockgen]    new    {file}"
    else:
        result = f"[blockgen]  changed  {file}"

    print(result)
