# Example: generate `to_string` implementations for C++ enums

This example demonstrates how to use `blockgen` to automatically generate `to_string` implementations for C++ enums.

In [`main.cpp`](main.cpp), each enum definition is followed by a `<<[ to_string_enum_impl("EnumName") ]>>` block, which serves as a placeholder for the generated `to_string` implementation of that enum:

```cpp
enum Enum1 {
    VALUE1,
    VALUE2,
    VALUE3,
};

// <<[ to_string_enum_impl("Enum1") ]>>
    // Generation will happen here
// <<[ end ]>>
```

Launching [`script.py`](script.py) will parse the enum definitions in [`main.cpp`](main.cpp) and generate the corresponding `to_string` implementations in the respective blocks.
