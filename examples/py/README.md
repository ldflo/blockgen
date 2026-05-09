# Example: generate a Django server from an OpenAPI schema

This example demonstrates how to use `blockgen` to generate a Django server from an OpenAPI schema, while preserving handwritten endpoint implementations across re-generations.

Launching [`script.py`](script.py) will generate the file [`server.py`](server.py) based on the OpenAPI schema defined in [`api.json`](api.json). The generated code includes placeholders for the implementation of each API endpoint, which can be manually filled in:

```python
def get(self, request, id):
   """ Get a todo by id """
   ### <<[ get_todo ]>>
   # TODO: Implement the logic for get_todo
   return JsonResponse({"message": "not implemented"}, status=501)
   ### <<[ end ]>>
```

When [`script.py`](script.py) is run again, it will preserve any manual edits made to the implementation sections, allowing for iterative development without losing custom code, thanks to [`blockgen.file.write_and_reinject_blocks`](../../docs/doc_blockgen.md#blockgenfilewrite_and_reinject_blocksfile-text--encodingnone-newlinenone-mkdirtrue).

The script will also generate a Jupyter notebook [`client.ipynb`](client.ipynb) with code snippets for testing the API endpoints, which can also be manually edited and preserved across future re-generations when new endpoints are added. Considering that Jupyter notebooks are in JSON format, re-injection of previous cells is done with JSON operations instead of [`blockgen.file.write_and_reinject_blocks`](../../docs/doc_blockgen.md#blockgenfilewrite_and_reinject_blocksfile-text--encodingnone-newlinenone-mkdirtrue).
