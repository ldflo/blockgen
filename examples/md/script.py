import blockgen

class MdUtils:
    def parse_functions_definition(self, filepath: str) -> list[tuple[str, int]]:
        with open(filepath, "r") as f:
            content = f.read()
        functions = []
        for lineno, line in enumerate(content.splitlines(), start=1):
            if line.startswith("def "):
                function_name = line.split("def ")[1].split("(")[0].strip()
                functions.append((function_name, lineno))
        return functions

    @blockgen.callback("string_links")
    def string_links_callback(self):
        # Step 1: Extract the function definitions from string.py
        string_functions = self.parse_functions_definition("../../src/blockgen/string.py")

        # Step 2: Generate the Markdown links
        result = ""
        for function_name, lineno in string_functions:
            result += f"- [`{function_name}`](../../src/blockgen/string.py#L{lineno})\n"
        return result[:-1] # Strip trailing newline

    @blockgen.callback("file_links")
    def file_links_callback(self):
        # Step 1: Extract the function definitions from file.py
        file_functions = self.parse_functions_definition("../../src/blockgen/file.py")

        # Step 2: Generate the Markdown links
        result = ""
        for function_name, lineno in file_functions:
            result += f"- [`{function_name}`](../../src/blockgen/file.py#L{lineno})\n"
        return result[:-1] # Strip trailing newline

blocks = {"*": MdUtils()}
blockgen.file.set_blocks("./README.md", blocks)
