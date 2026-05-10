# Documentation

## Table of content

- [Blocks](#blocks)
  - [Syntax](#syntax)
  - [Indentation](#indentation)
  - [Nested blocks](#nested-blocks)
- [String functions](#string-functions)
  - [`blockgen.string.has_blocks`](#blockgenstringhas_blockstext)
  - [`blockgen.string.parse_blocks`](#blockgenstringparse_blockstext)
  - [`blockgen.string.list_blocks`](#blockgenstringlist_blockstext)
  - [`blockgen.string.get_blocks`](#blockgenstringget_blockstext)
  - [`blockgen.string.set_blocks`](#blockgenstringset_blockstext-blocks)
  - [`blockgen.string.replace_blocks`](#blockgenstringreplace_blockstext-blocks)
  - [`blockgen.string.remove_markers`](#blockgenstringremove_markerstext)
- [File functions](#file-functions)
  - [`blockgen.file.has_blocks`](#blockgenfilehas_blocksfile--encodingnone)
  - [`blockgen.file.parse_blocks`](#blockgenfileparse_blocksfile--encodingnone)
  - [`blockgen.file.list_blocks`](#blockgenfilelist_blocksfile--encodingnone)
  - [`blockgen.file.get_blocks`](#blockgenfileget_blocksfile--encodingnone)
  - [`blockgen.file.set_blocks`](#blockgenfileset_blocksfile-blocks--encodingnone-newlinenone)
  - [`blockgen.file.replace_blocks`](#blockgenfilereplace_blocksfile-blocks--encodingnone-newlinenone)
  - [`blockgen.file.remove_markers`](#blockgenfileremove_markersfile--encodingnone-newlinenone)
  - [`blockgen.file.write_and_reinject_blocks`](#blockgenfilewrite_and_reinject_blocksfile-text--encodingnone-newlinenone-mkdirtrue)
- [Options](#options)
  - [Marker literals](#marker-literals)
  - [Reinjection safeguard](#reinjection-safeguard)
  - [Console notifications](#console-notifications)

# Blocks

## Syntax

Blocks are sections of a file delimited by the `<<[ block_expression ]>>` and `<<[ end ]>>` markers:

```
Multiline block:

    <<[ block_expression ]>>
    block_content
    <<[ end ]>>

    // <<[ block_expression ]>>
    block_content
    // <<[ end ]>>

Inline block:

    <<[ block_expression ]>> block_content <<[ end ]>>

    /*<<[ block_expression ]>>*/ block_content /*<<[ end ]>>*/

Terminology:

    Open marker:          <<[
    Close marker:         ]>>
    Opening block marker: <<[ block_expression ]>>
    Ending block marker:  <<[ end ]>>

Block expression syntax:

    block_name
    block_name('a', 1, param=[1, 2, 3])
```

Each block expression must be unique in the file, otherwise an exception will be raised:

```python
import blockgen

text = """
// <<[ block1 ]>>
block1 content
// <<[ end ]>>

// <<[ block2('a', 1, param=[1, 2, 3]) ]>>
block2 content
// <<[ end ]>>
"""

blocks: dict[str, str] = blockgen.string.get_blocks(text)
assert blocks["block1"] == "block1 content"
assert blocks["block2('a', 1, param=[1, 2, 3])"] == "block2 content"
```

Block expressions follow the same syntax as Python function calls, to allow easy binding to Python functions when using the [`set_blocks`](#blockgenstringset_blockstext-blocks) function:

```python
import blockgen

text = """
// <<[ block1(1, 2) ]>>
// <<[ end ]>>

// <<[ block1(3, 5) ]>>
// <<[ end ]>>
"""

new_blocks = {
    "block1": lambda arg1, arg2: f"new content: {arg1 + arg2}"
}
new_text = blockgen.string.set_blocks(text, new_blocks)

assert new_text == """
// <<[ block1(1, 2) ]>>
new content: 3
// <<[ end ]>>

// <<[ block1(3, 5) ]>>
new content: 8
// <<[ end ]>>
"""
```

Note that only literal parameters are allowed (strings, numbers, booleans, lists, tuples, dicts, `None`, ...), and that calculation or variable reference are not possible:

```
<<[ block(1 + 2, sys.argv[0]) ]>> ❌ Not allowed
```

You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["`, `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`, and `BLOCKGEN_END_BLOCK_EXPRESSION="end"` or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>', end_block_expression='end')`:

```python
import blockgen

text = """
    // <<< block1 >>>
    content
    // <<< blockend >>>
"""

with blockgen.options(open_marker_literal='<<<', close_marker_literal='>>>', end_block_expression='blockend'):
    blocks: dict[str, str] = blockgen.string.get_blocks(text)
    assert blocks["block1"] == "content"
```

See the [Marker literals](#marker-literals) section for more information.

## Indentation

For multiline blocks, the indentation of the block content is automatically adjusted based on the open marker location and its preceding comment characters :

```python
import blockgen

text = """
<<[ block1 ]>>
<<[ end ]>>

// <<[ block2 ]>>
// <<[ end ]>>

    /* <<[ block3 ]>> */
    /* <<[ end ]>> */

        ### <<[ block4 ]>>
        ### <<[ end ]>> <<[ block5 ]>>
        ### <<[ end ]>>
"""

new_blocks = {
    "block1": "line1\nline2",
    "block2": "line3\nline4",
    "block3": "line5\nline6",
    "block4": "line7\nline8",
    "block5": "line9\nline10",
}
new_text = blockgen.string.set_blocks(text, new_blocks)

assert new_text == """
<<[ block1 ]>>
line1
line2
<<[ end ]>>

// <<[ block2 ]>>
line3
line4
// <<[ end ]>>

    /* <<[ block3 ]>> */
    line5
    line6
    /* <<[ end ]>> */

        ### <<[ block4 ]>>
        line7
        line8
        ### <<[ end ]>> <<[ block5 ]>>
        line9
        line10
        ### <<[ end ]>>
"""

blocks = blockgen.string.get_blocks(new_text)
assert blocks["block1"] == "line1\nline2"
assert blocks["block2"] == "line3\nline4"
assert blocks["block3"] == "line5\nline6"
assert blocks["block4"] == "line7\nline8"
assert blocks["block5"] == "line9\nline10"
```

## Nested blocks

Nested blocks are considered as part of the content of their parent block and will be treated as regular text:

```python
import blockgen

text = """
// <<[ block1 ]>>

    // <<[ block2 ]>>
    line1
    line2
    // <<[ end ]>>

// <<[ end ]>>
"""

blocks = blockgen.string.get_blocks(text)
assert len(blocks) == 1
assert blocks["block1"] == """
    // <<[ block2 ]>>
    line1
    line2
    // <<[ end ]>>
"""
```

# String functions

## `blockgen.string.has_blocks(text)`

Checks whether the given string contains at least one block marker.

Parameters:
- `text: str`: The string to search for block markers.

Returns:
- `bool`: `True` if the string contains at least one block marker, `False` otherwise.

Examples:

```python
import blockgen

text = """
// <<[ block1 ]>>
// <<[ end ]>>
"""

assert blockgen.string.has_blocks(text) == True

text = """
// <<[ block1 ]>>
"""

assert blockgen.string.has_blocks(text) == True
```

## `blockgen.string.parse_blocks(text)`

Parses all blocks found in the given string, yielding them one by one.

Parameters:
- `text: str`: The string to parse for blocks.

Yields:
- [`blockgen.Block`](../src/blockgen/core.py#L15): Each block found in the string, in order of appearance.

Examples:

```python
import blockgen

text = """
    // <<[ block1(1, 2) ]>>
    line1
    line2
    // <<[ end ]>>
"""

for block in blockgen.string.parse_blocks(text):
    assert block.name == "block1"
    assert block.args == [1, 2]
    assert block.indentation == "    "
```

## `blockgen.string.list_blocks(text)`

Returns the list of all blocks found in the given string.

Parameters:
- `text: str`: The string to parse for blocks.

Returns:
- [`list[blockgen.Block]`](../src/blockgen/core.py#L15): A list of all blocks found in the string, in order of appearance.

Examples:

```python
import blockgen

text = """
    // <<[ block1(1, 2) ]>>
    line1
    line2
    // <<[ end ]>>
"""

blocks = blockgen.string.list_blocks(text)
assert blocks[0].name == "block1"
assert blocks[0].args == [1, 2]
assert blocks[0].indentation == "    "
```

## `blockgen.string.get_blocks(text)`

Returns a dictionary of all blocks found in the given string.

Parameters:
- `text: str`: The string to parse for blocks.

Returns:
- `dict[str, str]`: A dictionary mapping each block expression to its content, in order of appearance.

Examples:

```python
import blockgen

text = """
// <<[ block1 ]>>
line1
line2
// <<[ end ]>>

// <<[ block2('a', 1, param=[1, 2, 3]) ]>>
line3
line4
// <<[ end ]>>
"""

blocks = blockgen.string.get_blocks(text)
assert blocks["block1"] == "line1\nline2"
assert blocks["block2('a', 1, param=[1, 2, 3])"] == "line3\nline4"
```

## `blockgen.string.set_blocks(text, blocks)`

Sets the content of the specified blocks in the given string.

Parameters:
- `text: str`: The string containing the blocks to update.
- `blocks: dict[str, Union[str, FunctionType, object, Type, None]]`: A dictionary mapping block expressions to their new content.

  The given keys can be:
  - A block name, e.g. `"block1"`
  - A full parameterized block expression, e.g. `"block1('a', 1, param=[1, 2, 3])"`
  - The `"*"` to match all remaining blocks not matched by a more specific key

  For block names or the `"*"` wildcard, values can be:
  - `None`: leaves the block content unchanged
  - A `str`: used directly as the new block content
  - A function `(*args, **kwargs) -> Optional[str]`: return value used as the new block content
  - A class instance with [`@blockgen.callback("block_name")`](../src/blockgen/core.py#L120) decorated methods `(self, *args, **kwargs) -> Optional[str]`: return value used as the new block content
  - A class type with [`@blockgen.callback("block_name")`](../src/blockgen/core.py#L120) decorated static methods `(*args, **kwargs) -> Optional[str]`: return value used as the new block content

  For full parameterized block expressions, values can be:
  - `None`: leaves the block content unchanged
  - A `str`: used directly as the new block content

Returns:
- `str`: A new string with the specified block contents replaced.

Notes:
- Use `blockgen.current_block` to access the current [`blockgen.Block`](../src/blockgen/core.py#L15) object from within callbacks.

Examples:

```python
import blockgen

text = """
// <<[ block1 ]>>
// <<[ end ]>>

// <<[ block2(3, 4) ]>>
// <<[ end ]>>

// <<[ block2(5, 6) ]>>
// <<[ end ]>>
"""

### Example 1

new_blocks = {
    "block1": "line1\nline2",
    "block2": "line3\nline4",
}
new_text = blockgen.string.set_blocks(text, new_blocks)

assert new_text == """
// <<[ block1 ]>>
line1
line2
// <<[ end ]>>

// <<[ block2(3, 4) ]>>
line3
line4
// <<[ end ]>>

// <<[ block2(5, 6) ]>>
line3
line4
// <<[ end ]>>
"""

### Example 2

new_blocks = {
    "block1": "line1\nline2",
    "block2": lambda arg1, arg2: f"line{arg1}\nline{arg2}",
}
new_text = blockgen.string.set_blocks(text, new_blocks)

assert new_text == """
// <<[ block1 ]>>
line1
line2
// <<[ end ]>>

// <<[ block2(3, 4) ]>>
line3
line4
// <<[ end ]>>

// <<[ block2(5, 6) ]>>
line5
line6
// <<[ end ]>>
"""

### Example 3

new_blocks = {
    "*": "line1\nline2",
    "block2(3, 4)": "line3\nline4",
}
new_text = blockgen.string.set_blocks(text, new_blocks)

assert new_text == """
// <<[ block1 ]>>
line1
line2
// <<[ end ]>>

// <<[ block2(3, 4) ]>>
line3
line4
// <<[ end ]>>

// <<[ block2(5, 6) ]>>
line1
line2
// <<[ end ]>>
"""

### Example 4

new_blocks = {
    "*": lambda *args, **kwargs: f"{blockgen.current_block.name}({', '.join(map(str, args))})"
}
new_text = blockgen.string.set_blocks(text, new_blocks)

assert new_text == """
// <<[ block1 ]>>
block1()
// <<[ end ]>>

// <<[ block2(3, 4) ]>>
block2(3, 4)
// <<[ end ]>>

// <<[ block2(5, 6) ]>>
block2(5, 6)
// <<[ end ]>>
"""

### Example 5

class CustomClass:
    @blockgen.callback("block2")
    def block2_callback(self, arg1: int, arg2: int) -> Optional[str]:
        return f"line{arg1}\nline{arg2}"

new_blocks = {
    "block1": "line1\nline2",
    "block2": CustomClass(),
}
new_text = blockgen.string.set_blocks(text, new_blocks)

assert new_text == """
// <<[ block1 ]>>
line1
line2
// <<[ end ]>>

// <<[ block2(3, 4) ]>>
line3
line4
// <<[ end ]>>

// <<[ block2(5, 6) ]>>
line5
line6
// <<[ end ]>>
"""

### Example 6

class CustomClass:
    @staticmethod
    @blockgen.callback("block1")
    def block1_callback(*args, **kwargs) -> Optional[str]:
        return "line1\nline2"

    @staticmethod
    @blockgen.callback("block2")
    def block2_callback(arg1: int, arg2: int) -> Optional[str]:
        return f"line{arg1}\nline{arg2}"

new_blocks = {
    "*": CustomClass,
    "block2(3, 4)": "new content",
}
new_text = blockgen.string.set_blocks(text, new_blocks)

assert new_text == """
// <<[ block1 ]>>
line1
line2
// <<[ end ]>>

// <<[ block2(3, 4) ]>>
new content
// <<[ end ]>>

// <<[ block2(5, 6) ]>>
line5
line6
// <<[ end ]>>
"""

### Example 7

class CustomClass:
    @blockgen.callback("*")
    def block1_callback(self, *args, **kwargs) -> Optional[str]:
        return blockgen.current_block.name

    @blockgen.callback("block2")
    def block2_callback(self, arg1: int, arg2: int) -> Optional[str]:
        return f"line{arg1}\nline{arg2}"

new_blocks = {
    "*": CustomClass()
}
new_text = blockgen.string.set_blocks(text, new_blocks)

assert new_text == """
// <<[ block1 ]>>
block1
// <<[ end ]>>

// <<[ block2(3, 4) ]>>
line3
line4
// <<[ end ]>>

// <<[ block2(5, 6) ]>>
line5
line6
// <<[ end ]>>
"""
```

## `blockgen.string.replace_blocks(text, blocks)`

Replaces the content of the specified blocks in the given string. Uses a safeguard that raises an error if any of the specified blocks is not found in the string.
You can disable the safeguard with the environment variable `BLOCKGEN_DISABLE_SAFEGUARD="1"` or with `blockgen.options(disable_safeguard=True)`. See the [Reinjection safeguard](#reinjection-safeguard) section for more information.

Parameters:
- `text: str`: The string containing the blocks to update.
- `blocks: dict[str, Union[str, None]]`: A dictionary mapping block expressions to their new content.

  The given keys must be the same exact block expressions of the blocks in the string.

  The value `None` leaves the block content unchanged.

Returns:
- `str`: A new string with the specified block contents replaced.

Examples:

```python
import blockgen

text = """
// <<[ block1 ]>>
// <<[ end ]>>

// <<[ block2(3, 4) ]>>
// <<[ end ]>>

// <<[ block2(5, 6) ]>>
// <<[ end ]>>
"""

### Example 1

new_blocks = {
    "block1": "line1\nline2",
    "block2(3, 4)": "line3\nline4",
    "block2(5, 6)": "line5\nline6",
}
new_text = blockgen.string.replace_blocks(text, new_blocks)

assert new_text == """
// <<[ block1 ]>>
line1
line2
// <<[ end ]>>

// <<[ block2(3, 4) ]>>
line3
line4
// <<[ end ]>>

// <<[ block2(5, 6) ]>>
line5
line6
// <<[ end ]>>
"""

### Example 2

with blockgen.options(disable_safeguard=True):
    new_blocks = {
        "block1": "line1\nline2",
        "block2(3, 4)": "line3\nline4",
        "block2(5, 6)": "line5\nline6",
        "block67": "non existing block",
    }
    # Doesn't raise an error even if "block67" is not found in the string
    new_text = blockgen.string.replace_blocks(text, new_blocks)
```

## `blockgen.string.remove_markers(text)`

Removes all block markers from the given string, keeping only the block contents.

Parameters:
- `text: str`: The string containing the block markers to remove.

Returns:
- `str`: A new string with all block markers removed and only the block contents retained.

Examples:

```python
assert text == """
int value = /*<<[ block1 ]>>*/ 42 /*<<[ end ]>>*/;

    // <<[ block2 ]>>
    line1
    line2
    // <<[ end ]>> <<[ block3 ]>>
    line3
    line4
    // <<[ end ]>>
"""

new_text = blockgen.string.remove_markers(text)
assert new_text == """
int value = 42;

    line1
    line2
    line3
    line4
"""
```

# File functions

## `blockgen.file.has_blocks(file, *, encoding=None)`

File equivalent of [`blockgen.string.has_blocks`](#blockgenstringhas_blockstext).
Checks whether the given file contains at least one block marker.

Parameters:
- `file: Union[str, os.PathLike]`: The file to search for block markers.
- `encoding: Optional[str]`: The encoding used when reading the file.

Returns:
- `bool`: `True` if at least one block marker is found, `False` otherwise.

Examples:

```python
import blockgen

has_blocks: bool = blockgen.file.has_blocks("/path/to/file.txt")
```

## `blockgen.file.parse_blocks(file, *, encoding=None)`

File equivalent of [`blockgen.string.parse_blocks`](#blockgenstringparse_blockstext).
Parses all blocks found in the given file, yielding them one by one.

Parameters:
- `file: Union[str, os.PathLike]`: The file to parse for blocks.
- `encoding: Optional[str]`: The encoding used when reading the file.

Yields:
- [`blockgen.Block`](../src/blockgen/core.py#L15): Each block found in the file, in order of appearance.

Examples:

```python
import blockgen

for block in blockgen.file.parse_blocks("/path/to/file.txt"):
    ...
```

## `blockgen.file.list_blocks(file, *, encoding=None)`

File equivalent of [`blockgen.string.list_blocks`](#blockgenstringlist_blockstext).
Returns the list of all blocks found in the given file.

Parameters:
- `file: Union[str, os.PathLike]`: The file to parse for blocks.
- `encoding: Optional[str]`: The encoding used when reading the file.

Returns:
- [`list[blockgen.Block]`](../src/blockgen/core.py#L15): A list of all blocks found in the file, in order of appearance.

Examples:

```python
import blockgen

blocks: list[blockgen.Block] = blockgen.file.list_blocks("/path/to/file.txt")
```

## `blockgen.file.get_blocks(file, *, encoding=None)`

File equivalent of [`blockgen.string.get_blocks`](#blockgenstringget_blockstext).
Returns a dictionary of all blocks found in the given file.

Parameters:
- `file: Union[str, os.PathLike]`: The file to parse for blocks.
- `encoding: Optional[str]`: The encoding used when reading the file.

Returns:
- `dict[str, str]`: A dictionary mapping each block expression to its content, in order of appearance.

Examples:

```python
import blockgen

blocks: dict[str, str] = blockgen.file.get_blocks("/path/to/file.txt")
```

## `blockgen.file.set_blocks(file, blocks, *, encoding=None, newline=None)`

File equivalent of [`blockgen.string.set_blocks`](#blockgenstringset_blockstext-blocks).
Sets the content of the specified blocks in the given file.
If the file content is the same, the file is left unchanged to avoid unnecessary file modification.

Parameters:
- `file: Union[str, os.PathLike]`: The file containing the blocks to update.
- `blocks: dict[str, Union[str, FunctionType, object, Type, None]]`: See [`blockgen.string.set_blocks`](#blockgenstringset_blockstext-blocks) for the full description.
- `encoding: Optional[str]`: The encoding used when reading and writing the file.
- `newline: Optional[str]`: The newline character(s) used when writing the file.

Returns:
- `str`: The new file content with the specified block contents replaced.

Notes:
- Use `blockgen.current_block` to access the current [`blockgen.Block`](../src/blockgen/core.py#L15) object from within callbacks.
- Use `blockgen.current_filepath` to access the current filepath from within callbacks.

Examples:

```python
import blockgen

new_blocks = {
    "block1": "line1\nline2",
    "*": lambda *args, **kwargs: f"{blockgen.current_block.name}({', '.join(map(str, args))})",
}
blockgen.file.set_blocks("/path/to/file.txt", new_blocks)
```

## `blockgen.file.replace_blocks(file, blocks, *, encoding=None, newline=None)`

File equivalent of [`blockgen.string.replace_blocks`](#blockgenstringreplace_blockstext-blocks).
Replaces the content of the specified blocks in the given file. Uses a safeguard that raises an error if any of the specified blocks is not found in the file.
If the file content is the same, the file is left unchanged to avoid unnecessary file modification.
You can disable the safeguard with the environment variable `BLOCKGEN_DISABLE_SAFEGUARD="1"` or with `blockgen.options(disable_safeguard=True)`. See the [Reinjection safeguard](#reinjection-safeguard) section for more information.

Parameters:
- `file: Union[str, os.PathLike]`: The file containing the blocks to update.
- `blocks: dict[str, Union[str, None]]`: See [`blockgen.string.replace_blocks`](#blockgenstringreplace_blockstext-blocks) for the full description.
- `encoding: Optional[str]`: The encoding used when reading and writing the file.
- `newline: Optional[str]`: The newline character(s) used when writing the file.

Returns:
- `str`: The new file content with the specified block contents replaced.

Examples:

```python
import blockgen

new_blocks = {
    "block1": "line1\nline2",
    "block2(3, 4)": "line3\nline4",
    "block2(5, 6)": "line5\nline6",
}
blockgen.file.replace_blocks("/path/to/file.txt", new_blocks)
```

## `blockgen.file.remove_markers(file, *, encoding=None, newline=None)`

File equivalent of [`blockgen.string.remove_markers`](#blockgenstringremove_markerstext).
Removes all block markers from the given file, keeping only the block contents.
If the file content is the same, the file is left unchanged to avoid unnecessary file modification.

Parameters:
- `file: Union[str, os.PathLike]`: The file containing the block markers to remove.
- `encoding: Optional[str]`: The encoding used when reading and writing the file.
- `newline: Optional[str]`: The newline character(s) used when writing the file.

Returns:
- `str`: The new file content with all block markers removed and only the block contents retained.

Examples:

```python
import blockgen

blockgen.file.remove_markers("/path/to/file.txt")
```

## `blockgen.file.write_and_reinject_blocks(file, text, *, encoding=None, newline=None, mkdir=True)`

Writes the given text to the file and reinjects the old block contents from the file into the new text.
If the file does not exist yet, the text is written as-is.
If the file content is the same, the file is left unchanged to avoid unnecessary file modification.
Uses a safeguard that raises an error if any old block from the existing file cannot be reinjected in the new text.
You can disable the safeguard with the environment variable `BLOCKGEN_DISABLE_SAFEGUARD="1"` or with `blockgen.options(disable_safeguard=True)`. See the [Reinjection safeguard](#reinjection-safeguard) section for more information.

Equivalent to:
```python
old_blocks = blockgen.file.get_blocks(file)
with open(file, "w") as f:
    f.write(text)
blockgen.file.replace_blocks(file, old_blocks)
```

Parameters:
- `file: Union[str, os.PathLike]`: The file to write to and reinject blocks into.
- `text: str`: The text to write to the file.
- `encoding: Optional[str]`: The encoding used when reading and writing the file.
- `newline: Optional[str]`: The newline character(s) used when writing the file.
- `mkdir: bool`: If `True` (default), creates parent directories of the file if they do not exist.

Returns:
- `str`: The written text, with the old block contents reinjected.

Examples:

```python
import blockgen

### Write the file

text = """
// <<[ block1 ]>>
line1
line2
// <<[ end ]>>
"""

blockgen.file.write_and_reinject_blocks("/path/to/file.txt", text)

with open("/path/to/file.txt") as f:
    new_text = f.read()

assert new_text == """
// <<[ block1 ]>>
line1
line2
// <<[ end ]>>
"""

### Update the file

text = """
// <<[ block1 ]>>
// <<[ end ]>>
// <<[ block2 ]>>
// <<[ end ]>>
"""

blockgen.file.write_and_reinject_blocks("/path/to/file.txt", text)

with open("/path/to/file.txt") as f:
    new_text = f.read()

assert new_text == """
// <<[ block1 ]>>
line1
line2
// <<[ end ]>>
// <<[ block2 ]>>
// <<[ end ]>>
"""
```

# Options

## Marker literals

By default, blocks are delimited by the `<<[ block_expression ]>>` and `<<[ end ]>>` markers.

You can change the marker literals used with the environment variables `BLOCKGEN_OPEN_MARKER_LITERAL="<<["`, `BLOCKGEN_CLOSE_MARKER_LITERAL="]>>"`, and `BLOCKGEN_END_BLOCK_EXPRESSION="end"` or with `blockgen.options(open_marker_literal='<<[', close_marker_literal=']>>', end_block_expression='end')`:

```python
import blockgen

### Example 1

import os
os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"] = "[[["
os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"] = "]]]"
os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"] = "@@@"

text = """
[[[ block1 ]]]
line1
line2
[[[ @@@ ]]]
"""

blocks = blockgen.string.get_blocks(text)
assert blocks["block1"] == "line1\nline2"

### Example 2

text = """
<<< block1 >>>
line1
line2
<<< blockend >>>
"""

with blockgen.options(open_marker_literal='<<<',
                      close_marker_literal='>>>',
                      end_block_expression='blockend'):
    blocks = blockgen.string.get_blocks(text)
    assert blocks["block1"] == "line1\nline2"
```

## Reinjection safeguard

The functions [`blockgen.string.replace_blocks`](#blockgenstringreplace_blockstext-blocks), [`blockgen.file.replace_blocks`](#blockgenfilereplace_blocksfile-blocks--encodingnone-newlinenone) and [`blockgen.file.write_and_reinject_blocks`](#blockgenfilewrite_and_reinject_blocksfile-text--encodingnone-newlinenone-mkdirtrue) are intended to maintain handwritten blocks inside generated files. They use a safeguard that raises an error if any previous block wasn't properly reused in the new text, to prevent accidental loss of handwritten content:

```python
import blockgen

### Write the file

text = """
// <<[ block1 ]>>
line1
line2
// <<[ end ]>>
"""

blockgen.file.write_and_reinject_blocks("/path/to/file.txt", text)

### Update the file

text = """
// <<[ block2 ]>>
// <<[ end ]>>
"""

# Raises an error, content of "block1" will be lost
blockgen.file.write_and_reinject_blocks("/path/to/file.txt", text)
```

If you really intend to get rid of the existing block contents, you can disable the safeguard with the environment variable `BLOCKGEN_DISABLE_SAFEGUARD="1"` or with `blockgen.options(disable_safeguard=True)`:

```python
### Example 1

import os
os.environ["BLOCKGEN_DISABLE_SAFEGUARD"] = "1"

# "block1" is purposely lost, no error is raised
blockgen.file.write_and_reinject_blocks("/path/to/file.txt", text)

### Example 2

with blockgen.options(disable_safeguard=True):
    # "block1" is purposely lost, no error is raised
    blockgen.file.write_and_reinject_blocks("/path/to/file.txt", text)
```

## Console notifications

All the file write operations performed by `blockgen` print a notification to the console indicating whether the file was created, changed, or left unchanged:

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

```python
import blockgen

### Example 1

import os
os.environ["BLOCKGEN_NOTIFY_ABSOLUTE_PATH"] = "0"

blockgen.file.set_blocks("/path/to/file.txt", blocks)

### Example 2

with blockgen.options(notify_absolute_path=False):
    blockgen.file.set_blocks("/path/to/file.txt", blocks)
```

You can disable these notifications with the environment variable `BLOCKGEN_SILENT="1"` or with `blockgen.options(silent=True)`.

```python
import blockgen

### Example 1

import os
os.environ["BLOCKGEN_SILENT"] = "1"

# No notification is printed to the console
blockgen.file.set_blocks("/path/to/file.txt", blocks)

### Example 2

with blockgen.options(silent=True):
    # No notification is printed to the console
    blockgen.file.set_blocks("/path/to/file.txt", blocks)
```
