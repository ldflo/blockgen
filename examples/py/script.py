import blockgen
from functools import cached_property
import json
import os
from typing import Any

class PyUtils:
    @cached_property
    def open_api_json(self):
        with open("./api.json") as f:
            return json.load(f)

    def viewclass_name(self, path):
        return path.strip("/").title().replace("/", "_").replace("{", "").replace("}", "") + "View"

    def path_parameters(self, operation_item: dict[str, Any]):
        for parameter in operation_item.get("parameters", []):
            if parameter["in"] == "path":
                yield parameter["name"], parameter

    def body_parameters(self, operation_item: dict[str, Any]):
        for name, parameter in operation_item.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {}).get("properties", {}).items():
            yield name, parameter

    ###
    ### For server.py generation
    ###

    def generate_server_class_views(self) -> str:
        classes = []
        for path, path_item in self.open_api_json["paths"].items():
            class_lines = []
            class_lines.append(f'@method_decorator(csrf_exempt, name="dispatch")')
            class_lines.append(f'class {self.viewclass_name(path)}(View):')
            # Generate methods for each HTTP method
            operations = []
            for method, operation_item in path_item.items():
                operations_lines = []
                operations_lines.append(f'    def {method}(self, request, {", ".join([name for name, _ in self.path_parameters(operation_item)])}):')
                operations_lines.append(f'        """ {operation_item.get("summary", "No description")} """')
                operations_lines.append(f'        ### <<[ {operation_item["operationId"]} ]>>')
                operations_lines.append(f'        # TODO: Implement the logic for {operation_item["operationId"]}')
                operations_lines.append(f'        return JsonResponse({{"message": "not implemented"}}, status=501)')
                operations_lines.append(f'        ### <<[ end ]>>')
                operations.append('\n'.join(operations_lines))
            class_lines.append('\n\n'.join(operations))
            classes.append('\n'.join(class_lines))
        return '\n\n'.join(classes)

    def generate_server_url_patterns(self) -> str:
        urls = []
        for path, path_item in self.open_api_json["paths"].items():
            # Compute the URL pattern, replacing path parameters like {id} with Django's <int:id>
            method, operation_item = next(iter(path_item.items()))
            url_path = path.strip('/')
            for name, parameter in self.path_parameters(operation_item):
                if parameter["schema"]["type"] == "string":
                    url_path = url_path.replace(f'{{{name}}}', f'<str:{name}>')
                elif parameter["schema"]["type"] == "number":
                    url_path = url_path.replace(f'{{{name}}}', f'<float:{name}>')
                elif parameter["schema"]["type"] == "integer":
                    url_path = url_path.replace(f'{{{name}}}', f'<int:{name}>')
                elif parameter["schema"]["type"] == "boolean":
                    url_path = url_path.replace(f'{{{name}}}', f'<bool:{name}>')
            urls.append(f'path("{url_path}", {self.viewclass_name(path)}.as_view()),')
        return '\n'.join(urls)

    ###
    ### For client.ipynb generation
    ###

    @cached_property
    def previous_ipynb_cells(self) -> dict[str, dict[str, Any]]: # operationId -> cell
        result = {}
        if os.path.isfile("./client.ipynb"):
            with open("./client.ipynb", "r") as f:
                json_content = json.load(f)

            for cell in json_content["cells"]:
                if cell["cell_type"] == "code":
                    if "id" in cell["metadata"]:
                        cell_id = cell["metadata"]["id"]
                        result[cell_id] = cell
        return result

    def generate_ipynb_json(self) -> str:
        json_content = {
            "cells": [],
            "metadata": {
                "language_info": {
                    "name": "python"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }
        for path, path_item in self.open_api_json["paths"].items():
            for method, operation_item in path_item.items():
                # Markdown cell
                markdown_cell = {
                    "cell_type": "markdown",
                    "metadata": {
                        # Used to identify the cell for potential reuse of content in future generations
                        "id": f"{operation_item['operationId']}"
                    },
                    "source": [
                        f'# {operation_item["operationId"]}'
                    ],
                }
                json_content["cells"].append(markdown_cell)

                # Code cell
                code_cell = {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {
                        # Used to identify the cell for potential reuse of content in future generations
                        "id": f"{operation_item['operationId']}"
                    },
                    "outputs": [],
                    "source": [],
                }
                if operation_item["operationId"] in self.previous_ipynb_cells:
                    # Reuse the previous code cell content if the operationId matches, to preserve any manual edits
                    code_cell["source"] = self.previous_ipynb_cells[operation_item["operationId"]]["source"]
                else:
                    code_cell["source"].append(f'""" {operation_item.get("summary", "No description")} """\n')
                    code_cell["source"].append(f'import requests\n')
                    code_cell["source"].append(f'\n')
                    code_cell["source"].append(f'BASE_URL = "http://127.0.0.1:8000"\n')
                    code_cell["source"].append(f'\n')
                    for name, parameter in self.path_parameters(operation_item):
                        if parameter["schema"]["type"] == "string":
                            code_cell["source"].append(f'{name}: str = "..." # Change me\n')
                        elif parameter["schema"]["type"] == "number":
                            code_cell["source"].append(f'{name}: float = 0.0 # Change me\n')
                        elif parameter["schema"]["type"] == "integer":
                            code_cell["source"].append(f'{name}: int = 0 # Change me\n')
                        elif parameter["schema"]["type"] == "boolean":
                            code_cell["source"].append(f'{name}: bool = False # Change me\n')
                    body_parameters = list(self.body_parameters(operation_item))
                    if body_parameters:
                        code_cell["source"].append(f'body = {{\n')
                        for name, parameter in body_parameters:
                            if parameter["type"] == "string":
                                code_cell["source"].append(f'    "{name}": "...", # Change me\n')
                            elif parameter["type"] == "number":
                                code_cell["source"].append(f'    "{name}": 0.0, # Change me\n')
                            elif parameter["type"] == "integer":
                                code_cell["source"].append(f'    "{name}": 0, # Change me\n')
                            elif parameter["type"] == "boolean":
                                code_cell["source"].append(f'    "{name}": False, # Change me\n')
                        code_cell["source"].append(f'}}\n')
                        code_cell["source"].append(f'response = requests.{method}(f"{{BASE_URL}}{path}", json=body)\n')
                    else:
                        code_cell["source"].append(f'response = requests.{method}(f"{{BASE_URL}}{path}")\n')
                    code_cell["source"].append(f'print(response.status_code)\n')
                    code_cell["source"].append(f'print(response.text)')
                json_content["cells"].append(code_cell)

        return json.dumps(json_content, indent=1)

utils = PyUtils()

###
### Generate server.py
###

text = f"""### ⚠️ Auto-generated, edit only the sections between the blockgen markers.

import django
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import path
import sys

### <<[ custom_imports ]>>
# Place your imports here
### <<[ end ]>>

{utils.generate_server_class_views()}

urlpatterns = [
    {utils.generate_server_url_patterns().replace('\n', "\n    ")}
]

if __name__ == "__main__":
    from django.conf import settings
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
    )
    django.setup()

    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "runserver", "127.0.0.1:8000"] + sys.argv[1:])
"""

blockgen.file.write_and_reinject_blocks("./server.py", text, encoding="utf-8")

###
### Generate client.ipynb
###

text = utils.generate_ipynb_json()

blockgen.file.atomic_write("./client.ipynb", text, encoding="utf-8")
