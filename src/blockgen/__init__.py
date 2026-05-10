__version__ = "1.1.0"

from .core import (
    Block,
    callback,
    Context,
    current_context,
    context,
    Options,
    current_options,
    options,
    get_env_BLOCKGEN_OPEN_MARKER_LITERAL,
    get_env_BLOCKGEN_CLOSE_MARKER_LITERAL,
    get_env_BLOCKGEN_END_BLOCK_EXPRESSION,
    get_env_BLOCKGEN_DISABLE_SAFEGUARD,
    get_env_BLOCKGEN_SILENT,
    get_env_BLOCKGEN_NOTIFY_ABSOLUTE_PATH,
    set_env_BLOCKGEN_OPEN_MARKER_LITERAL,
    set_env_BLOCKGEN_CLOSE_MARKER_LITERAL,
    set_env_BLOCKGEN_END_BLOCK_EXPRESSION,
    set_env_BLOCKGEN_DISABLE_SAFEGUARD,
    set_env_BLOCKGEN_SILENT,
    set_env_BLOCKGEN_NOTIFY_ABSOLUTE_PATH,
    BaseException,
    UnmatchedBlockEndMarkerError,
    MissingBlockEndMarkerError,
    MissingSpacesBetweenBlockMarkersError,
    NamelessBlockError,
    BlockExpressionError,
    DuplicatedBlockExpressionError,
    CallbackDecoratorBlockNameError,
    DuplicatedCallbackDecoratorBlockNameError,
    InvalidValueTypeError,
    CallbackNotFoundError,
    BlockCallbackError,
    BlockContentError,
    NonReplacedBlockError,
    NonReinjectedBlockError,
)
from . import file
from . import string

###
### Helpers
###

import os
from typing import Optional, Union

""" Used to access the current block information from within callbacks. """
current_block: Optional[Block]
""" Used to access the current filepath from within callbacks for file operations. """
current_filepath: Optional[Union[str, os.PathLike]]

def __getattr__(name: str):
    if name == "current_filepath":
        return current_context.get().filepath
    if name == "current_block":
        return current_context.get().block
    raise AttributeError(f"module 'blockgen' has no attribute '{name}'")
