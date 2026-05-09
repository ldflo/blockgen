import blockgen

def create_block(expression: str) -> blockgen.Block:
    open_match = blockgen.BLOCKGEN_OPTIONS.get().get_block_regex().search(f"<<[ {expression} ]>>")
    block = blockgen.Block(open_match)
    blockgen.core._parse_block_name_args_kwargs(block, expression)
    return block

class Test:

    def test_1(self):
        block = create_block("""myBlock1""")
        assert block.expression == "myBlock1"
        assert block.name == "myBlock1"
        assert block.args == []
        assert block.kwargs == {}

        block = create_block("""myBlock1('a', 1, 'c')""")
        assert block.expression == "myBlock1('a', 1, 'c')"
        assert block.name == "myBlock1"
        assert block.args == ['a', 1, 'c']
        assert block.kwargs == {}

        block = create_block("""myBlock1('a', 1, 'c', d=4)""")
        assert block.expression == "myBlock1('a', 1, 'c', d=4)"
        assert block.name == "myBlock1"
        assert block.args == ['a', 1, 'c']
        assert block.kwargs == {'d': 4}

        block = create_block("""myBlock1('a', 1.0, 'c')""")
        assert block.expression == "myBlock1('a', 1.0, 'c')"
        assert block.name == "myBlock1"
        assert block.args == ['a', 1.0, 'c']
        assert block.kwargs == {}

        block = create_block("""myBlock1('a', 1.0, [1, 2, 3])""")
        assert block.expression == "myBlock1('a', 1.0, [1, 2, 3])"
        assert block.name == "myBlock1"
        assert block.args == ['a', 1.0, [1, 2, 3]]
        assert block.kwargs == {}

        block = create_block("""myBlock1('a', 1.0, [1, 2, {'x': 9, 'y': 8}])""")
        assert block.expression == "myBlock1('a', 1.0, [1, 2, {'x': 9, 'y': 8}])"
        assert block.name == "myBlock1"
        assert block.args == ['a', 1.0, [1, 2, {'x': 9, 'y': 8}]]
        assert block.kwargs == {}

    def test_2(self):
        block = create_block("""myBlock1 """)
        assert block.expression == "myBlock1"
        assert block.name == "myBlock1"
        assert block.args == []
        assert block.kwargs == {}

        block = create_block("""myBlock1 ( 'a' , 1 , 'c' ) """)
        assert block.expression == "myBlock1('a', 1, 'c')"
        assert block.name == "myBlock1"
        assert block.args == ['a', 1, 'c']
        assert block.kwargs == {}

        block = create_block("""myBlock1 ( 'a' , 1.0 , 'c' ) """)
        assert block.expression == "myBlock1('a', 1.0, 'c')"
        assert block.name == "myBlock1"
        assert block.args == ['a', 1.0, 'c']
        assert block.kwargs == {}

        block = create_block("""myBlock1 ( 'a' , 1.0 , 'c', d = 4 ) """)
        assert block.expression == "myBlock1('a', 1.0, 'c', d=4)"
        assert block.name == "myBlock1"
        assert block.args == ['a', 1.0, 'c']
        assert block.kwargs == {'d': 4}

        block = create_block("""myBlock1 ( 'a' , 1.0 , [ 1 , 2 , 3 ] ) """)
        assert block.expression == "myBlock1('a', 1.0, [1, 2, 3])"
        assert block.name == "myBlock1"
        assert block.args == ['a', 1.0, [1, 2, 3]]
        assert block.kwargs == {}

        block = create_block("""myBlock1 ( 'a' , 1.0, [ 1, 2, { 'x' : 9, 'y' : 8 } ] ) """)
        assert block.expression == "myBlock1('a', 1.0, [1, 2, {'x': 9, 'y': 8}])"
        assert block.name == "myBlock1"
        assert block.args == ['a', 1.0, [1, 2, {'x': 9, 'y': 8}]]
        assert block.kwargs == {}
