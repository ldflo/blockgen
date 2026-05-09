#include <cassert>
#include <iostream>
#include <string>

enum Enum1 {
    VALUE1,
    VALUE2,
    VALUE3,
};

// <<[ to_string_enum_impl("Enum1") ]>>
std::string to_string(Enum1 value) {
    // Auto-generated, do not modify manually
    switch(value) {
        case VALUE1: return "VALUE1";
        case VALUE2: return "VALUE2";
        case VALUE3: return "VALUE3";
        default: return "Enum1(" + std::to_string(static_cast<int>(value)) + ")";
    }
}
// <<[ end ]>>

enum Enum2 {
    VAL_1 = 0b0001,
    VAL_2 = 0b0010,
    VAL_3 = 0b0100,
    VAL_4 = 0b1000,
};

// <<[ to_string_enum_impl("Enum2") ]>>
std::string to_string(Enum2 value) {
    // Auto-generated, do not modify manually
    switch(value) {
        case VAL_1: return "VAL_1";
        case VAL_2: return "VAL_2";
        case VAL_3: return "VAL_3";
        case VAL_4: return "VAL_4";
        default: return "Enum2(" + std::to_string(static_cast<int>(value)) + ")";
    }
}
// <<[ end ]>>

void main() {
    assert(to_string(Enum1::VALUE1) == "VALUE1");
    assert(to_string(Enum2::VAL_3) == "VAL_3");
}
