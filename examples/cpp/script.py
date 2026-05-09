import blockgen
import re

class CppUtils:
    @blockgen.callback("to_string_enum_impl")
    def to_string_enum_impl_callback(self, enum_name: str):
        # Step 1: Extract the enum identifers using a simple regex
        with open(blockgen.current_filepath, "r") as f:
            content = f.read()
        pattern = rf"enum\s+{enum_name}\s*{{(.*?)}};"
        match = re.search(pattern, content, re.DOTALL)
        enum_definitions = [v.strip() for v in match.group(1).split(",") if v.strip()]
        enum_identifiers = [v.split("=")[0].strip() for v in enum_definitions]

        # Step 2: Generate the to_string implementation
        result = f"std::string to_string({enum_name} value) {{\n"
        result += "    // Auto-generated, do not modify manually\n"
        result += "    switch(value) {\n"
        for identifier in enum_identifiers:
            result += f"        case {identifier}: return \"{identifier}\";\n"
        result += f"        default: return \"{enum_name}(\" + std::to_string(static_cast<int>(value)) + \")\";\n"
        result += "    }\n"
        result += "}"
        return result

blocks = {"*": CppUtils()}
blockgen.file.set_blocks("./main.cpp", blocks)
