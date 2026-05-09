# Example: generate links in this Markdown file

This example demonstrates how to use `blockgen` to inject content inside Markdown files.

Launching [`script.py`](script.py) will parse the content of [`src/blockgen/string.py`](../src/blockgen/string.py) and [`src/blockgen/file.py`](../src/blockgen/file.py) to create the following links to all the functions defined in these files:

## String functions
<!-- <<[ string_links ]>> -->
- [`has_blocks`](../../src/blockgen/string.py#L6)
- [`parse_blocks`](../../src/blockgen/string.py#L32)
- [`list_blocks`](../../src/blockgen/string.py#L113)
- [`get_blocks`](../../src/blockgen/string.py#L152)
- [`set_blocks`](../../src/blockgen/string.py#L194)
- [`replace_blocks`](../../src/blockgen/string.py#L322)
- [`remove_markers`](../../src/blockgen/string.py#L396)
<!-- <<[ end ]>> -->

## File functions
<!-- <<[ file_links ]>> -->
- [`has_blocks`](../../src/blockgen/file.py#L11)
- [`parse_blocks`](../../src/blockgen/file.py#L46)
- [`list_blocks`](../../src/blockgen/file.py#L99)
- [`get_blocks`](../../src/blockgen/file.py#L150)
- [`set_blocks`](../../src/blockgen/file.py#L201)
- [`replace_blocks`](../../src/blockgen/file.py#L344)
- [`remove_markers`](../../src/blockgen/file.py#L434)
- [`write_and_reinject_blocks`](../../src/blockgen/file.py#L509)
- [`atomic_write`](../../src/blockgen/file.py#L627)
- [`notify_modification_in_console`](../../src/blockgen/file.py#L723)
<!-- <<[ end ]>> -->
