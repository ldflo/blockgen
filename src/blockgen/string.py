from types import FunctionType
from typing import Generator, Optional, Type, Union

from . import core

def has_blocks(
    text: str
) -> bool:
    """ Checks whether the given string contains at least one block marker.

        Parameters
        ----------
        text: str
            The string to search for block markers.

        Returns
        -------
        bool
            `True` if at least one block marker is found, `False` otherwise.

        Notes
        -----
        By default, a block marker is of the form `<<[ block_expression ]>>`.

        You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["` and `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`
        or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>')`.
    """
    cfg = core.current_options.get()
    block_regex = cfg.get_block_regex()
    return block_regex.search(text) is not None

def parse_blocks(
    text: str
) -> Generator[core.Block, None, None]:
    """ Parses all blocks found in the given string, yielding them one by one.

        Parameters
        ----------
        text: str
            The string to parse for blocks.

        Yields
        ------
        blockgen.Block
            Each block found in the string, in order of appearance.

        Raises
        ------
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
    cfg = core.current_options.get()
    block_regex = cfg.get_block_regex()
    end_block_expression = cfg.get_end_block_expression()
    current_block: Optional[core.Block] = None
    seen_block_expressions: set[str] = set()
    depth = 0

    for match in block_regex.finditer(text):
        raw_block_expression = match.group(1)
        if current_block is None:
            # Outside any block
            if raw_block_expression == end_block_expression:
                raise core._exception_unmatched_block_end_marker(match)
            # Opening a new block
            if raw_block_expression == "":
                raise core._exception_nameless_block(match)
            current_block = core.Block(match)
            core._parse_block_name_args_kwargs(current_block, raw_block_expression)
            if current_block.expression in seen_block_expressions:
                raise core._exception_duplicated_block_expression(current_block)
            seen_block_expressions.add(current_block.expression)
        else:
            if raw_block_expression != end_block_expression:
                # Nested block: ignore, treat as content
                depth += 1
            elif depth > 0:
                # Closing a nested block, treat as content
                depth -= 1
            else:
                # Closing current block
                current_block.end_match = match
                core._resolve_is_inline_block(current_block)
                if current_block.is_inline:
                    core._extract_inline_block_content(current_block)
                    yield current_block
                else: # Multiline block
                    core._extract_multiline_block_indentation(current_block)
                    core._extract_multiline_block_content(current_block)
                    yield current_block
                current_block = None

    if current_block is not None:
        raise core._exception_missing_block_end_marker(current_block)

def list_blocks(
    text: str
) -> list[core.Block]:
    """ Returns the list of all blocks found in the given string.

        Parameters
        ----------
        text: str
            The string to parse for blocks.

        Returns
        -------
        list[blockgen.Block]
            A list of all blocks found in the string, in order of appearance.

        Raises
        ------
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
    return list(parse_blocks(text))

def get_blocks(
    text: str
) -> dict[str, str]:
    """ Returns a dictionary of all blocks found in the given string.

        Parameters
        ----------
        text: str
            The string to parse for blocks.

        Returns
        -------
        dict[str, str]
            A dictionary mapping each block expression to its content, in order of appearance.

        Raises
        ------
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
    blocks: dict[str, str] = {}
    for block in parse_blocks(text):
        blocks[block.expression] = block.content
    return blocks

def set_blocks(
    text: str,
    blocks: dict[str, Union[str, FunctionType, object, Type, None]],
) -> str:
    """ Sets the content of the specified blocks in the given string.

        Parameters
        ----------
        text: str
            The string containing the blocks to update.
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

        Returns
        -------
        str
            A new string with the specified block contents replaced.

        Raises
        ------
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

        By default, a block is of the form `<<[ block_expression ]>> block_content <<[ end ]>>`.

        You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["`, `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`, and `BLOCKGEN_END_BLOCK_EXPRESSION="end"`
        or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>', end_block_expression='end')`.

        Examples
        --------
        ```
        class InstanceClass:
            @blockgen.callback("block3")
            def callback(self, *args, **kwargs) -> Optional[str]:
                return "new content"

            @blockgen.callback("*")
            def generic_callback(self, *args, **kwargs) -> Optional[str]:
                return f"new content for {blockgen.current_block.name}"

        class StaticClass:
            @staticmethod
            @blockgen.callback("block3")
            def callback(*args, **kwargs) -> Optional[str]:
                return "new content"

            @staticmethod
            @blockgen.callback("*")
            def generic_callback(*args, **kwargs) -> Optional[str]:
                return f"new content for {blockgen.current_block.name}"

        blocks = {
            "block1('a', 1, param=[1, 2, 3])": "new content",
            "block2": lambda *args, **kwargs: f"new content for {blockgen.current_block.name}",
            "*": InstanceClass(),
            # Alternatively
            # "*": StaticClass,
        }
        new_text = blockgen.string.set_blocks(text, blocks)
        ```
    """
    # Bind block callbacks
    callbacks = core._bind_block_callbacks(blocks)

    new_text: list[str] = []
    pos = 0

    for block in parse_blocks(text):
        new_text.append(text[pos:block.open_extended_end])
        new_content = core._compute_block_content(block, callbacks)
        if new_content is None:
            new_text.append(block.raw_content)
        elif block.is_inline:
            if '\n' in new_content:
                raise core._exception_block_content_error(block)
            new_text.append(' ')
            new_text.append(new_content)
            new_text.append(' ')
        elif new_content != "":
            new_indented_content = core._indent_block_content(new_content, block.indentation)
            new_text.append(new_indented_content)
        pos = block.end_extended_start

    new_text.append(text[pos:])
    return ''.join(new_text)

def replace_blocks(
    text: str,
    blocks: dict[str, Union[str, None]],
) -> str:
    """ Replaces the content of the specified blocks in the given string.
        Uses a safeguard that raises an error if any of the specified blocks is not found in the string.

        Parameters
        ----------
        text: str
            The string containing the blocks to update.
        blocks: dict[str, Union[str, None]]
            A dictionary mapping block expressions to their new content.

            The given keys must be the same exact block expressions of the blocks in the string.

            The value `None` leaves the block content unchanged.

        Returns
        -------
        str
            A new string with the specified block contents replaced.

        Raises
        ------
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
            If at least one of the specified blocks is not found in the string.

        Notes
        -----
        By default, a block is of the form `<<[ block_expression ]>> block_content <<[ end ]>>`.

        You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["`, `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`, and `BLOCKGEN_END_BLOCK_EXPRESSION="end"`
        or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>', end_block_expression='end')`.

        You can disable the safeguard with the environment variable `BLOCKGEN_DISABLE_SAFEGUARD="1"`
        or with `blockgen.options(disable_safeguard=True)`.
    """
    cfg = core.current_options.get()

    # Verify that all specified blocks can be found in the text
    if not cfg.get_disable_safeguard():
        old_blocks = list_blocks(text)
        missing_block_expressions: list[str] = []
        for new_block_expression in blocks:
            found = False
            for old_block in old_blocks:
                if old_block.expression == new_block_expression:
                    found = True
                    break
                if old_block.raw_expression == new_block_expression:
                    found = True
                    break
            if not found:
                missing_block_expressions.append(new_block_expression)
        if len(missing_block_expressions) > 0:
            raise core._exception_non_replaced_block(missing_block_expressions)

    return set_blocks(text, blocks)

def remove_markers(
    text: str
) -> str:
    """ Removes all block markers from the given string, keeping only the block contents.

        Parameters
        ----------
        text: str
            The string containing the block markers to remove.

        Returns
        -------
        str
            A new string with all block markers removed and only the block contents retained.

        Raises
        ------
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
    new_text: list[str] = []
    pos = 0

    blocks = list_blocks(text)
    for idx, block in enumerate(blocks):
        if block.is_inline:
            if pos < block.end_extended_end:
                new_text.append(text[pos:block.open_extended_start])
                new_text.append(block.content)
                pos = block.end_extended_end
        else:
            start = text.rfind('\n', pos, block.open_extended_start)+1
            if start > pos:
                new_text.append(text[pos:start])
            elif idx > 0:
                # Special case: <<[ block ]>> inline <<[ end ]>> <<[ block2 ]>>\n
                previous_block = blocks[idx - 1]
                if previous_block.is_inline and start < previous_block.end_extended_end:
                    new_text.append('\n')
            new_text.append(block.raw_content)
            end = text.find('\n', block.end_extended_end)
            if end < 0:
                end = len(text)
            elif idx == len(blocks) - 1:
                end += 1
            else:
                # Special case: \n<<[ end ]>> <<[ block2 ]>> inline <<[ end ]>>
                next_block = blocks[idx + 1]
                if next_block.is_inline and end > next_block.open_extended_start:
                    new_text.append(block.indentation)
                    end = next_block.open_extended_start
                else:
                    end += 1
            pos = end

    new_text.append(text[pos:])
    return ''.join(new_text)
