import ast
import contextlib
import contextvars
import dataclasses
import functools
import os
import re
import sys
from types import FunctionType, MethodType
from typing import Any, Callable, Optional, Tuple, Union

__dataclass_slots = {"slots": True} if sys.version_info >= (3, 10) else {}

@dataclasses.dataclass(eq=False, init=False, **__dataclass_slots)
class Block:
    """ Represents a parsed block from a source string.

        A block is delimited by an open marker and an end marker:
            **Inline form**:
            ```
            /*<<[ block_expression ]>>*/ block_content /*<<[ end ]>>*/
            ```

            **Multiline form**:
            ```
            // <<[ block_expression ]>>
            block_content
            // <<[ end ]>>
            ```

        Block expressions consist of a block name followed by optional arguments, just like Python function call expressions:

            ```
            <<[ block1 ]>>
            <<[ block1('a', 1, param=[1, 2, 3]) ]>>
            ```

        Arguments must be valid Python literals (strings, numbers, booleans, lists, tuples, dicts, `None`, ...).

        Attributes
        ----------
        open_match: re.Match[str]
            The regex match object for the opening marker, e.g. `<<[ block1 ]>>`.
        end_match: re.Match[str]
            The regex match object for the ending marker, e.g. `<<[ end ]>>`.
        raw_expression: str
            The raw block expression string as it appears in the source, e.g. `block1` or `block1 ('a',1,param=[1, 2, 3])`.
        expression: str
            The normalized block expression, as produced by `ast.unparse`, e.g. `block1` or `block1('a', 1, param=[1, 2, 3])`.
        name: str
            The block name, e.g. `block1`.
        args: list[Any]
            The positional arguments of the block expression, e.g. `['a', 1]` for `block1('a', 1, param=[1, 2, 3])`.
        kwargs: dict[str, Any]
            The keyword arguments of the block expression, e.g. `{'param': [1, 2, 3]}` for `block1('a', 1, param=[1, 2, 3])`.
        is_inline: bool
            `True` if the block is on a single line, `False` if it spans multiple lines.
        open_extended_start: int
            Start position of the opening block marker in the source string.
        open_extended_end: int
            End position of the opening block marker in the source string (exclusive).
        end_extended_start: int
            Start position of the ending block marker in the source string.
        end_extended_end: int
            End position of the ending block marker in the source string (exclusive).
        indentation: str
            The indentation string (spaces or tabs) prepended to each line of block content.
        is_open_marker_indentation: bool
            `True` if the indentation was determined from the open marker position, `False` if from the end marker position.
        raw_content: str
            The raw block content as it appears in the source string, without de-indentation.
        content: str
            The block content with indentation stripped.

        Properties
        ----------
        string: str
            The full source string containing the block.
        is_multiline: bool
            `True` if the block spans multiple lines (i.e. `not is_inline`).

        Notes
        -----
        By default, a block is of the form `<<[ block_expression ]>> block_content <<[ end ]>>`.

        You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["`, `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`, and `BLOCKGEN_END_BLOCK_EXPRESSION="end"`
        or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>', end_block_expression='end')`.
    """
    open_match: re.Match[str]
    end_match: re.Match[str]
    raw_expression: str
    expression: str
    name: str
    args: list[Any]
    kwargs: dict[str, Any]
    is_inline: bool
    open_extended_start: int
    open_extended_end: int
    end_extended_start: int
    end_extended_end: int
    indentation: str
    is_open_marker_indentation: bool
    raw_content: str
    content: str

    def __init__(self, open_match: re.Match[str]) -> None:
        self.open_match = open_match

    @property
    def string(self) -> str:
        return self.open_match.string
    @property
    def is_multiline(self) -> bool:
        return not self.is_inline

###
### Callback decorator for binding blocks to methods or static methods
###

def callback(block_name: str):
    """ Decorator to bind a method or a static method to a block name, for use with `set_blocks`.

        Parameters
        ----------
        block_name: str
            The block name to bind to, e.g. `"block1"`.
            Use `"*"` to match all remaining blocks not matched by a more specific callback.

        Raises
        ------
        blockgen.CallbackDecoratorBlockNameError
            If the block name is invalid.

        Notes
        -----
        For an instance method, the callback signature must be:
        ```
        @blockgen.callback("block_name")
        def callback(self, *args, **kwargs) -> Optional[str]:
            ...
        ```

        For a static method, the callback signature must be:
        ```
        @staticmethod
        @blockgen.callback("block_name")
        def callback(*args, **kwargs) -> Optional[str]:
            ...
        ```

        Use `blockgen.current_block` to access the current `blockgen.Block` object from within the callback.
        Use `blockgen.current_filepath` to access the current filepath from within the callback for file operations.

        Examples
        --------
        ```
        class InstanceClass:
            @blockgen.callback("block1")
            def callback(self, *args, **kwargs) -> Optional[str]:
                return f"new content inside {blockgen.current_filepath}"

            @blockgen.callback("*")
            def generic_callback(self, *args, **kwargs) -> Optional[str]:
                return f"new content for {blockgen.current_block.name}"

        class StaticClass:
            @staticmethod
            @blockgen.callback("block1")
            def callback(*args, **kwargs) -> Optional[str]:
                return f"new content inside {blockgen.current_filepath}"

            @staticmethod
            @blockgen.callback("*")
            def generic_callback(*args, **kwargs) -> Optional[str]:
                return f"new content for {blockgen.current_block.name}"

        blocks = {
            "*": InstanceClass(),
            # Alternatively
            # "*": StaticClass,
        }
        new_text = blockgen.file.set_blocks(filepath, blocks)
        ```
    """
    def wrapper(func: Callable[..., Optional[str]]):
        # Validate block name
        if block_name != "*" and not block_name.isidentifier():
            raise _exception_callback_decorator_block_name(block_name)
        setattr(func, "__blockgen_decorator_callback_block_name", block_name)
        return func
    return wrapper

###
### Context
###

@dataclasses.dataclass(eq=False, frozen=True, **__dataclass_slots)
class Context:
    """ Immutable object representing the context of the block currently being processed by a callback.

        Attributes
        ----------
        block: blockgen.Block
            The block currently being processed.
            Use `blockgen.current_block` inside a callback.
        filepath: Optional[Union[str, os.PathLike]]
            The path of the file being processed, or `None` if the operation is on a string.
            Use `blockgen.current_filepath` inside a callback.
    """
    block: Block
    filepath: Optional[Union[str, os.PathLike]] = None

# ContextVar so nested/async contexts are isolated
BLOCKGEN_CONTEXT: contextvars.ContextVar[Context] = contextvars.ContextVar("BLOCKGEN_CONTEXT", default=Context(block=None))

@contextlib.contextmanager
def context(
    *,
    block: Optional[Block] = None,
    filepath: Optional[Union[str, os.PathLike]] = None,
):
    """ Context manager that temporarily sets the blockgen context for the duration of the `with` block.

        The context is restored to its previous value when the `with` block exits, even if an exception is raised.
        Nesting is supported: inner `with blockgen.context(...)` blocks further override the current context.

        Parameters
        ----------
        block: Optional[blockgen.Block]
            The block currently being processed.
            Use `blockgen.current_block` inside a callback.
        filepath: Optional[Union[str, os.PathLike]]
            The path of the file being processed, or `None` if the operation is on a string.
            Use `blockgen.current_filepath` inside a callback.

        Examples
        --------
        ```
        with blockgen.context(block=block, filepath=filepath):
            result = callback(block)
        ```
    """
    cur_cfg = BLOCKGEN_CONTEXT.get()
    new_cfg = Context(
        block = block or cur_cfg.block,
        filepath = filepath or cur_cfg.filepath,
    )

    token = BLOCKGEN_CONTEXT.set(new_cfg)
    try:
        yield
    finally:
        BLOCKGEN_CONTEXT.reset(token)

###
### Options
###

@dataclasses.dataclass(frozen=True, **__dataclass_slots)
class Options:
    """ Immutable object for options with blockgen.

        All fields default to `None`, meaning the value will be read from the corresponding
        environment variable, or fall back to the built-in default if not set.

        Use `blockgen.options(...)` as a context manager to apply options for a block of code.

        Attributes
        ----------
        open_marker_literal: Optional[str]
            The literal string that opens a block marker. Default: `"<<["`.
        close_marker_literal: Optional[str]
            The literal string that closes a block marker. Default: `"]>>"`.
        end_block_expression: Optional[str]
            The block expression used as the end marker. Default: `"end"`.
        disable_safeguard: Optional[bool]
            If `True`, disables the safeguard of `replace_blocks` and `write_and_reinject_blocks`. Default: `False`.
        silent: Optional[bool]
            If `True`, suppresses console notifications after writing a file. Default: `False`.
        notify_absolute_path: Optional[bool]
            If `True`, prints absolute paths in console notifications instead of relative paths. Default: `True`.
    """
    open_marker_literal: Optional[str] = None
    close_marker_literal: Optional[str] = None
    end_block_expression: Optional[str] = None
    disable_safeguard: Optional[bool] = None
    silent: Optional[bool] = None
    notify_absolute_path: Optional[bool] = None

    def get_open_marker_literal(self) -> str:
        return self.open_marker_literal or get_env_BLOCKGEN_OPEN_MARKER_LITERAL() or "<<["
    def get_close_marker_literal(self) -> str:
        return self.close_marker_literal or get_env_BLOCKGEN_CLOSE_MARKER_LITERAL() or "]>>"
    def get_end_block_expression(self) -> str:
        return self.end_block_expression or get_env_BLOCKGEN_END_BLOCK_EXPRESSION() or "end"
    def get_disable_safeguard(self) -> bool:
        if self.disable_safeguard is not None:
            return self.disable_safeguard
        if get_env_BLOCKGEN_DISABLE_SAFEGUARD() is not None:
            return get_env_BLOCKGEN_DISABLE_SAFEGUARD()
        return False
    def get_silent(self) -> bool:
        if self.silent is not None:
            return self.silent
        if get_env_BLOCKGEN_SILENT() is not None:
            return get_env_BLOCKGEN_SILENT()
        return False
    def get_notify_absolute_path(self) -> bool:
        if self.notify_absolute_path is not None:
            return self.notify_absolute_path
        if get_env_BLOCKGEN_NOTIFY_ABSOLUTE_PATH() is not None:
            return get_env_BLOCKGEN_NOTIFY_ABSOLUTE_PATH()
        return True
    def get_block_regex(self) -> re.Pattern:
        return Options.__build_block_regex(self.get_open_marker_literal(), self.get_close_marker_literal())

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def __build_block_regex(open_marker_literal: str, close_marker_literal: str) -> re.Pattern:
        return re.compile(rf"{re.escape(open_marker_literal)}\s*(.*?)\s*{re.escape(close_marker_literal)}", re.DOTALL)

# ContextVar so nested/async contexts are isolated
BLOCKGEN_OPTIONS: contextvars.ContextVar[Options] = contextvars.ContextVar("BLOCKGEN_OPTIONS", default=Options())

@contextlib.contextmanager
def options(
    *,
    open_marker_literal: Optional[str] = None,
    close_marker_literal: Optional[str] = None,
    end_block_expression: Optional[str] = None,
    disable_safeguard: Optional[bool] = None,
    silent: Optional[bool] = None,
    notify_absolute_path: Optional[bool] = None,
):
    """ Context manager that temporarily overrides blockgen options for the duration of the `with` block.

        Options are restored to their previous values when the `with` block exits, even if an exception is raised.
        Nesting is supported: inner `with blockgen.options(...)` blocks further override the current options.

        Parameters
        ----------
        open_marker_literal: Optional[str]
            The literal string that opens a block marker.
        close_marker_literal: Optional[str]
            The literal string that closes a block marker.
        end_block_expression: Optional[str]
            The block expression used as the end marker.
        disable_safeguard: Optional[bool]
            If `True`, disables the safeguard of `replace_blocks` and `write_and_reinject_blocks`.
        silent: Optional[bool]
            If `True`, suppresses console notifications after writing a file.
        notify_absolute_path: Optional[bool]
            If `True`, prints absolute paths in console notifications instead of relative paths.

        Examples
        --------
        ```
        with blockgen.options(open_marker_literal='<!--', close_marker_literal='-->'):
            blocks = blockgen.file.get_blocks(file)
        ```
    """
    cur_cfg = BLOCKGEN_OPTIONS.get()
    new_cfg = Options(
        open_marker_literal = open_marker_literal or cur_cfg.open_marker_literal,
        close_marker_literal = close_marker_literal or cur_cfg.close_marker_literal,
        end_block_expression = end_block_expression or cur_cfg.end_block_expression,
        disable_safeguard = disable_safeguard if disable_safeguard is not None else cur_cfg.disable_safeguard,
        silent = silent if silent is not None else cur_cfg.silent,
        notify_absolute_path = notify_absolute_path if notify_absolute_path is not None else cur_cfg.notify_absolute_path,
    )

    token = BLOCKGEN_OPTIONS.set(new_cfg)
    try:
        yield
    finally:
        BLOCKGEN_OPTIONS.reset(token)

def get_env_BLOCKGEN_OPEN_MARKER_LITERAL() -> Optional[str]:
    return os.environ.get("BLOCKGEN_OPEN_MARKER_LITERAL")

def get_env_BLOCKGEN_CLOSE_MARKER_LITERAL() -> Optional[str]:
    return os.environ.get("BLOCKGEN_CLOSE_MARKER_LITERAL")

def get_env_BLOCKGEN_END_BLOCK_EXPRESSION() -> Optional[str]:
    return os.environ.get("BLOCKGEN_END_BLOCK_EXPRESSION")

def get_env_BLOCKGEN_DISABLE_SAFEGUARD() -> Optional[bool]:
    value = os.environ.get("BLOCKGEN_DISABLE_SAFEGUARD")
    if value is None:
        return None
    return value.lower() in ("1", "on", "true", "yes", "y")

def get_env_BLOCKGEN_SILENT() -> Optional[bool]:
    value = os.environ.get("BLOCKGEN_SILENT")
    if value is None:
        return None
    return value.lower() in ("1", "on", "true", "yes", "y")

def get_env_BLOCKGEN_NOTIFY_ABSOLUTE_PATH() -> Optional[bool]:
    value = os.environ.get("BLOCKGEN_NOTIFY_ABSOLUTE_PATH")
    if value is None:
        return None
    return value.lower() in ("1", "on", "true", "yes", "y")

def set_env_BLOCKGEN_OPEN_MARKER_LITERAL(value: Optional[str]):
    if value is not None:
        os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"] = value
    elif "BLOCKGEN_OPEN_MARKER_LITERAL" in os.environ:
        del os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"]

def set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(value: Optional[str]):
    if value is not None:
        os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"] = value
    elif "BLOCKGEN_CLOSE_MARKER_LITERAL" in os.environ:
        del os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"]

def set_env_BLOCKGEN_END_BLOCK_EXPRESSION(value: Optional[str]):
    if value is not None:
        os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"] = value
    elif "BLOCKGEN_END_BLOCK_EXPRESSION" in os.environ:
        del os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"]

def set_env_BLOCKGEN_DISABLE_SAFEGUARD(value: Optional[bool]):
    if value is not None:
        os.environ["BLOCKGEN_DISABLE_SAFEGUARD"] = "1" if value else "0"
    elif "BLOCKGEN_DISABLE_SAFEGUARD" in os.environ:
        del os.environ["BLOCKGEN_DISABLE_SAFEGUARD"]

def set_env_BLOCKGEN_SILENT(value: Optional[bool]):
    if value is not None:
        os.environ["BLOCKGEN_SILENT"] = "1" if value else "0"
    elif "BLOCKGEN_SILENT" in os.environ:
        del os.environ["BLOCKGEN_SILENT"]

def set_env_BLOCKGEN_NOTIFY_ABSOLUTE_PATH(value: Optional[bool]):
    if value is not None:
        os.environ["BLOCKGEN_NOTIFY_ABSOLUTE_PATH"] = "1" if value else "0"
    elif "BLOCKGEN_NOTIFY_ABSOLUTE_PATH" in os.environ:
        del os.environ["BLOCKGEN_NOTIFY_ABSOLUTE_PATH"]

###
### Exceptions
###

class BaseException(Exception):
    pass

class UnmatchedBlockEndMarkerError(BaseException):
    """ Raised when an ending block marker is found without a preceding opening block marker. """
    pass
class MissingBlockEndMarkerError(BaseException):
    """ Raised when an opening block marker has no matching ending block marker. """
    pass
class MissingSpacesBetweenBlockMarkersError(BaseException):
    """ Raised when there are no spaces between block markers. """
    pass
class NamelessBlockError(BaseException):
    """ Raised when an opening block marker has an empty block expression. """
    pass
class BlockExpressionError(BaseException):
    """ Raised when a block expression is invalid. """
    pass
class DuplicatedBlockExpressionError(BaseException):
    """ Raised when two blocks share the same (supposedly unique) expression. """
    pass
class CallbackDecoratorBlockNameError(BaseException):
    """ Raised when a block name used in a `@blockgen.callback` decorator is invalid. """
    pass
class DuplicatedCallbackDecoratorBlockNameError(BaseException):
    """ Raised when two `@blockgen.callback` decorators in the same class share the same block name. """
    pass
class InvalidValueTypeError(BaseException):
    """ Raised when a value given in the `blocks` dictionary is not of an allowed type. """
    pass
class CallbackNotFoundError(BaseException):
    """ Raised when no generic `@blockgen.callback("*")` is found on a class passed as a block value. """
    pass
class BlockCallbackError(BaseException):
    """ Raised when an error occurs while replacing a block content with a callback. """
    pass
class BlockContentError(BaseException):
    """ Raised when a new block content contains newlines but the block is inline. """
    pass
class NonReplacedBlockError(BaseException):
    """ Raised when at least one of the blocks specified in `replace_blocks` is not found in the string or file. """
    pass
class NonReinjectedBlockError(BaseException):
    """ Raised when at least one block from the existing file cannot be reinjected in the new text. """
    pass

def _exception_unmatched_block_end_marker(end_match: re.Match[str]) -> UnmatchedBlockEndMarkerError:
    line, col = _get_linecol(end_match.string, end_match.start())
    return UnmatchedBlockEndMarkerError(
        f"Unmatched block end marker '{end_match.group(0)}' at line {line}, column {col}"
    )

def _exception_missing_block_end_marker(block: Block) -> MissingBlockEndMarkerError:
    cfg = BLOCKGEN_OPTIONS.get()
    line, col = _get_linecol(block.string, block.open_match.start())
    return MissingBlockEndMarkerError(
        f"Missing block end marker '{cfg.get_open_marker_literal()} {cfg.get_end_block_expression()} {cfg.get_close_marker_literal()}' for block '{block.open_match.group(0)}' at line {line}, column {col}"
    )

def _exception_missing_spaces_between_block_markers(block: Block) -> MissingSpacesBetweenBlockMarkersError:
    cfg = BLOCKGEN_OPTIONS.get()
    line, col = _get_linecol(block.string, block.open_match.start())
    return MissingSpacesBetweenBlockMarkersError(
        f"Missing spaces between block markers '{block.open_match.string[block.open_extended_start:block.end_extended_end]}' at line {line}, column {col}" \
        f" (spaces are mandatory to make '/*{cfg.get_open_marker_literal()} block {cfg.get_close_marker_literal()}*/ ... /*{cfg.get_open_marker_literal()} {cfg.get_end_block_expression()} {cfg.get_close_marker_literal()}*/' style markers work)"
    )

def _exception_nameless_block(open_match: re.Match[str]) -> NamelessBlockError:
    line, col = _get_linecol(open_match.string, open_match.start())
    return NamelessBlockError(
        f"Nameless block '{open_match.group(0)}' at line {line}, column {col}"
    )

def _exception_block_expression(block: Block) -> BlockExpressionError:
    line, col = _get_linecol(block.string, block.open_match.start())
    return BlockExpressionError(
        f"Invalid block expression '{block.open_match.group(0)}' at line {line}, column {col}:\n"
        f"    1) look at the inner exception for more details\n"
        f"    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n"
        f"    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
    )

def _exception_duplicated_block_expression(block: Block) -> DuplicatedBlockExpressionError:
    line, col = _get_linecol(block.string, block.open_match.start())
    return DuplicatedBlockExpressionError(
        f"Duplicated block '{block.open_match.group(0)}' with same expression '{block.expression}' at line {line}, column {col}"
    )

def _exception_callback_decorator_block_name(block_name: str) -> CallbackDecoratorBlockNameError:
    return CallbackDecoratorBlockNameError(
        f"Invalid block name '{block_name}' used in callback decorator:\n"
        f"    1) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n"
        f"    2) you can also use '*' as block name to match all blocks\n"
        f"    3) parameters cannot be specified, only the block name is accepted"
    )

def _exception_duplicated_callback_decorator_block_name(block_name: str, obj: object) -> DuplicatedCallbackDecoratorBlockNameError:
    return DuplicatedCallbackDecoratorBlockNameError(
        f"Duplicated callback decorator for block '{block_name}' in {obj}"
    )

def _exception_invalid_value_type(block_name: str, obj: object) -> InvalidValueTypeError:
    return InvalidValueTypeError(
        f"Invalid value type '{type(obj)}' for block '{block_name}':\n"
        f"    1) values must be either a str, a function, a class instance or a class type\n"
        f"    2) classes can register instance methods and static methods thanks to the '@blockgen.callback' decorator"
    )

def _exception_callback_not_found(block: Block, obj: object) -> CallbackNotFoundError:
    return CallbackNotFoundError(
        f"Callback for block '{block.name}' not found in {obj}:\n"
        f"    1) you must decorate a method or a static method with '@blockgen.callback(\"block_name\")' or '@blockgen.callback(\"*\")'\n"
        f"    2) the method must have the signature '(self, *args, **kwargs) -> Optional[str]'\n"
        f"    3) the static method must have the signature '(*args, **kwargs) -> Optional[str]'"
    )

def _exception_block_callback(block: Block) -> BlockCallbackError:
    line, col = _get_linecol(block.string, block.open_match.start())
    return BlockCallbackError(
        f"An error occurred when replacing the content of block '{block.open_match.group(0)}' at line {line}, column {col}:\n"
        f"    1) look at the inner exception for more details\n"
        f"    2) make sure your function has the correct signature '(*args, **kwargs) -> Optional[str]'\n"
        f"    3) make sure your method has the correct signature '(self, *args, **kwargs) -> Optional[str]'\n"
        f"    4) make sure your static method has the correct signature '(*args, **kwargs) -> Optional[str]'"
    )

def _exception_block_content_error(block: Block) -> BlockContentError:
    line, col = _get_linecol(block.string, block.open_match.start())
    return BlockContentError(
        f"New content for inline block '{block.open_match.group(0)}' cannot contain newlines (\\n, \\r\\n or \\r) at line {line}, column {col}" \
    )

def _exception_non_replaced_block(missing_block_expressions: list[str]) -> NonReplacedBlockError:
    if len(missing_block_expressions) == 1:
        block_name = missing_block_expressions[0]
        message = f"Destination block not found, couldn't replace block '{block_name}'"
    else:
        message = f"Destination blocks not found, couldn't replace the following blocks:\n"
        for block_name in missing_block_expressions:
            message += f"    '{block_name}'\n"
        message = message[:-1] # Remove last newline
    return NonReplacedBlockError(message)

def _exception_non_reinjected_block(missing_blocks: list[Block]) -> NonReinjectedBlockError:
    if len(missing_blocks) == 1:
        block = missing_blocks[0]
        line, col = _get_linecol(block.string, block.open_match.start())
        message = f"Destination block not found, couldn't reinject block '{block.open_match.group(0)}' at line {line}, column {col}"
    else:
        message = f"Destination blocks not found, couldn't reinject the following blocks:\n"
        for block in missing_blocks:
            line, col = _get_linecol(block.string, block.open_match.start())
            message += f"    '{block.open_match.group(0)}' at line {line}, column {col}\n"
        message = message[:-1] # Remove last newline
    return NonReinjectedBlockError(message)

###
### Utility
###

def _get_linecol(string: str, pos: int) -> Tuple[int, int]:
    line = string.count('\n', 0, pos) + 1
    col = pos - string.rfind('\n', 0, pos)
    return line, col

def _parse_block_name_args_kwargs(block: Block, raw_block_expression: str) -> None:
    try:
        tree = ast.parse(raw_block_expression, mode="eval")
        block.raw_expression = raw_block_expression
        block.expression = ast.unparse(tree.body)
        if isinstance(tree.body, ast.Name):
            block.name = tree.body.id
            block.args = []
            block.kwargs = {}
        elif isinstance(tree.body, ast.Call):
            block.expression = ast.unparse(tree.body)
            block.name = tree.body.func.id
            block.args = [ast.literal_eval(arg) for arg in tree.body.args]
            kwargs: dict[str, Any] = {}
            for kwarg in tree.body.keywords:
                if kwarg.arg in kwargs:
                    raise SyntaxError(f"keyword argument repeated: {kwarg.arg}")
                kwargs[kwarg.arg] = ast.literal_eval(kwarg.value)
            block.kwargs = kwargs
        else:
            raise SyntaxError(f"unexpected type '{type(tree.body)}' for expression: {raw_block_expression}")
    except Exception as e:
        raise _exception_block_expression(block) from e

def _resolve_is_inline_block(block: Block) -> None:
    block.is_inline = block.string.find('\n', block.open_match.end(), block.end_match.start()) < 0
    if block.is_inline:
        block.open_extended_start, block.open_extended_end = _resolve_inline_open_marker_extension(block)
        block.end_extended_start, block.end_extended_end = _resolve_inline_end_marker_extension(block)
        if block.open_extended_end > block.end_extended_start:
            # Safety check to allow /*<<[ block ]>>*/ ... /*<<[ end ]>>*/ style markers
            raise _exception_missing_spaces_between_block_markers(block)
    else:
        block.open_extended_start, open_end = block.open_match.start(), block.open_match.end()
        end_start, block.end_extended_end = block.end_match.start(), block.end_match.end()
        block.open_extended_end = block.string.index('\n', open_end)+1
        block.end_extended_start = block.string.rindex('\n', block.open_extended_end-1, end_start)+1

def _resolve_inline_open_marker_extension(block: Block) -> Tuple[int, int]:
    cfg = BLOCKGEN_OPTIONS.get()
    close_marker_literal = cfg.get_close_marker_literal()
    string = block.string
    open_match_start = block.open_match.start()
    open_match_end = block.open_match.end()
    # Search for left marker extension '/*<<[ block ]>>'
    line_start = string.rfind('\n', 0, open_match_start)
    found = False
    for i in range(open_match_start-1, line_start, -1):
        c = string[i]
        if c == ' ' or c == '\t':
            found = True # Beginning of '/*' found
            break
    if not found:
        i = line_start
    idx = string.rfind(close_marker_literal, i+1, open_match_start)
    if idx < 0:
        start = i+1
    else:
        start = idx + len(close_marker_literal) # Without closing marker
    # Search for right marker extension '<<[ end ]>>*/'
    line_end = string.find('\n', open_match_end)
    if line_end < 0:
        line_end = len(string)
    found = False
    for i in range(open_match_end, line_end):
        c = string[i]
        if c == ' ' or c == '\t':
            found = True # Beginning of '/*' found
            break
    if not found:
        i = line_end
    end = i
    return start, end

def _resolve_inline_end_marker_extension(block: Block) -> Tuple[int, int]:
    cfg = BLOCKGEN_OPTIONS.get()
    open_marker_literal = cfg.get_open_marker_literal()
    string = block.string
    end_match_start = block.end_match.start()
    end_match_end = block.end_match.end()
    # Search for left marker extension '/*<<[ end ]>>'
    line_start = string.rfind('\n', 0, end_match_start)
    found = False
    for i in range(end_match_start-1, line_start, -1):
        c = string[i]
        if c == ' ' or c == '\t':
            found = True # Beginning of '/*' found
            break
    if not found:
        i = line_start
    start = i+1
    # Search for right marker extension '<<[ end ]>>*/'
    line_end = string.find('\n', end_match_end)
    if line_end < 0:
        line_end = len(string)
    found = False
    for i in range(end_match_end, line_end):
        c = string[i]
        if c == ' ' or c == '\t':
            found = True # Beginning of '/*' found
            break
    if not found:
        i = line_end
    idx = string.find(open_marker_literal, end_match_end, i)
    if idx < 0:
        end = i
    else:
        end = idx # Without opening marker
    return start, end

def _extract_inline_block_content(block: Block) -> None:
    raw_block_content = block.string[block.open_extended_end:block.end_extended_start]
    block_content = raw_block_content
    if block_content.startswith(' '):
        block_content = block_content[1:] # Remove first space
    if block_content.endswith(' '):
        block_content = block_content[:-1] # Remove last space
    block.raw_content = raw_block_content
    block.content = block_content

def _extract_multiline_block_indentation(block: Block) -> None:
    cfg = BLOCKGEN_OPTIONS.get()
    close_marker_literal = cfg.get_close_marker_literal()
    string = block.string

    # Resolve indentation based on open marker or end marker
    open_marker_start = block.open_match.start()
    open_line_start = string.rfind('\n', 0, open_marker_start)
    previous_close_marker_start = string.rfind(close_marker_literal, 0, open_marker_start)
    if open_line_start < previous_close_marker_start:
        marker_start = block.end_match.start()
        line_start = string.rfind('\n', 0, marker_start)
        block.is_open_marker_indentation = False
    else:
        marker_start = open_marker_start
        line_start = open_line_start
        block.is_open_marker_indentation = True

    if marker_start - line_start <= 1:
        indentation = "" # No indentation
    else:
        c = string[marker_start-1]
        if c == ' ' or c == '\t': # Indentation based on '// <<[ block ]>>'
            found = False # Search for presence of '//'
            for i in range(marker_start-1, line_start, -1):
                c = string[i]
                if c != ' ' and c != '\t':
                    found = True # Presence of '//' found
                    break
            if not found:
                end = marker_start # Indentation based on '<<[ block ]>>'
            else: # Presence of '//' found
                found = False # Search for beginning of '//'
                for j in range(i-1, line_start, -1):
                    c = string[j]
                    if c == ' ' or c == '\t':
                        found = True # Beginning of '//' found
                        break
                if not found:
                    j = line_start
                idx = string.rfind(close_marker_literal, j+1, i+1)
                if idx < 0:
                    end = j+1 # Indentation based on '// <<[ block ]>>'
                else:
                    end = marker_start # Indentation based on '<<[ block ]>>'
        else: # Indentation based on '/*<<[ block ]>>*/'
            found = False # Search for beginning of '/*'
            for i in range(marker_start-1, line_start, -1):
                c = string[i]
                if c == ' ' or c == '\t':
                    found = True # Beginning of '/*' found
                    break
            if not found:
                i = line_start
            idx = string.rfind(close_marker_literal, i+1, marker_start)
            if idx < 0:
                end = i+1 # Indentation based on '/*<<[ block ]>>*/'
            else:
                end = idx + len(close_marker_literal) # Indentation based on '/*<<[ block ]>>*/' without closing marker
        indentation = ''.join(['\t' if c == '\t' else ' ' for c in string[line_start+1:end]])
    block.indentation = indentation

def _extract_multiline_block_content(block: Block) -> None:
    # De-indent block content
    string = block.string
    indentation = block.indentation
    raw_block_content = string[block.open_extended_end:block.end_extended_start]
    deindented_content: list[str] = []
    for line in raw_block_content.splitlines(): # Skip first and last newlines
        if line.startswith(indentation):
            deindented_content.append(line[len(indentation):])
            deindented_content.append('\n')
        else:
            deindented_content.append(line.lstrip(' '))
            deindented_content.append('\n')
    block_content = ''.join(deindented_content)
    if block_content != "":
        block_content = block_content[:-1] # Remove last newline
    block.raw_content = raw_block_content
    block.content = block_content

def _bind_block_callbacks(blocks: dict[str, Union[str, FunctionType, object]]) -> dict[str, Callable[[Block], Optional[str]]]:
    # Inspect replacements for decorated callbacks
    replacement_decorator_callbacks: dict[int, dict[str, Union[FunctionType, MethodType]]] = {}
    for replacement in blocks.values():
        if replacement is None:
            continue # No replacement
        replacement_id = id(replacement)
        decorator_callbacks = replacement_decorator_callbacks.get(replacement_id)
        if decorator_callbacks is not None:
            continue # Already inspected
        decorator_callbacks = {}
        replacement_decorator_callbacks[replacement_id] = decorator_callbacks
        is_type = isinstance(replacement, type)
        # Inspect object for decorated callbacks
        for attrname in dir(replacement):
            if attrname.startswith("__"):
                continue # Ignore special methods
            attr = getattr(replacement, attrname)
            if is_type and not isinstance(attr, FunctionType):
                continue # Not a method
            decorator_block_name = getattr(attr, "__blockgen_decorator_callback_block_name", None)
            if decorator_block_name is None:
                continue # Not a decorated callback
            if decorator_block_name in decorator_callbacks:
                raise _exception_duplicated_callback_decorator_block_name(decorator_block_name, attr)
            decorator_callbacks[decorator_block_name] = attr

    # Bind block names to callbacks
    callbacks: dict[str, Callable[[Block], Optional[str]]] = {}
    for block_name, replacement in blocks.items():
        if replacement is None:
            continue # No replacement
        decorator_callbacks = replacement_decorator_callbacks[id(replacement)]
        if len(decorator_callbacks) > 0:
            attr = decorator_callbacks.get(block_name)
            if attr is not None:
                def callback_wrapper(
                    block: Block,
                    attr: Union[FunctionType, MethodType] = attr,
                ) -> Optional[str]:
                    return attr(*block.args, **block.kwargs)
                callbacks[block_name] = callback_wrapper

            else: # Generic callback
                def callback_wrapper(
                    block: Block,
                    obj: object = replacement,
                    decorator_callbacks: dict[str, Union[FunctionType, MethodType]] = decorator_callbacks
                ) -> Optional[str]:
                    callback = decorator_callbacks.get(block.name) or decorator_callbacks.get("*")
                    if callback is not None:
                        return callback(*block.args, **block.kwargs)
                    raise _exception_callback_not_found(block, obj)
                callbacks[block_name] = callback_wrapper

        elif isinstance(replacement, FunctionType):
            def callback_wrapper(
                block: Block,
                func: FunctionType = replacement,
            ) -> Optional[str]:
                return func(*block.args, **block.kwargs)
            callbacks[block_name] = callback_wrapper

        elif isinstance(replacement, str):
            def callback_wrapper(
                _: Block,
                string: str = replacement
            ) -> str:
                return string
            callbacks[block_name] = callback_wrapper

        else:
            raise _exception_invalid_value_type(block_name, replacement)
    return callbacks

def _compute_block_content(block: Block, callbacks: dict[str, Callable[[Block], Optional[str]]]) -> Optional[str]:
    callback = callbacks.get(block.name) \
            or callbacks.get(block.expression) \
            or callbacks.get(block.raw_expression) \
            or callbacks.get("*")
    if callback is not None:
        try:
            with context(block=block):
                result = callback(block)
            if result is not None:
                return str(result).replace("\r\n", '\n').replace('\r', '\n') # Normalize newlines
        except CallbackNotFoundError as e:
            raise e
        except Exception as e:
            raise _exception_block_callback(block) from e
    return None # No replacement found

def _indent_block_content(block_content: str, indentation: str) -> str:
    indented_block_content: list[str] = []
    lines = block_content.splitlines(keepends=True)
    for line in lines:
        if line.lstrip():
            indented_block_content.append(indentation)
            indented_block_content.append(line)
        elif line.endswith('\n'):
            indented_block_content.append('\n')
    # Special case to preserve spacing with only newlines
    for c in block_content:
        if c != '\n':
            indented_block_content.append('\n')
            break
    return ''.join(indented_block_content)
