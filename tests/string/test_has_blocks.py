import blockgen
import os

class Test_Inline:

    class Test_Inline_NominalCases:

        def test_1(self):
            text = """<<[ block1 ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_2(self):
            text = """<<[ block1 ]>>  <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_3(self):
            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_4(self):
            text = """<<[ block1 ]>>    abc    <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_5(self):
            text = """<<[block1]>> abc <<[end]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_6(self):
            text = """<<[   block1   ]>> abc <<[end]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_7(self):
            text = """<<[ block1 ]>> abc <<[ end ]>><<[ block2 ]>> def <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_8(self):
            text = """<<[ block1 ]>> abc <<[ end ]>> <<[ block2 ]>> def <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_9(self):
            text = """<<[ block1 ]>> abc <<[ end ]>>\n<<[ block2 ]>> def <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_10(self):
            # Block inside another block is considered part of the outer block
            text = """<<[ block1 ]>> abc <<[ block2 ]>> def <<[ end ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_11(self):
            # Empty block name inside another block is not considered an error
            text = """<<[ block1 ]>> abc <<[ ]>> def <<[ end ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_12(self):
            text = """/*<<[ block1 ]>>*/ /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_13(self):
            text = """/*<<[ block1 ]>>*/  /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_14(self):
            text = """/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_15(self):
            text = """/*<<[ block1 ]>>*/    abc    /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_16(self):
            text = """/*<<[block1]>>*/ abc /*<<[end]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_17(self):
            text = """/*<<[   block1   ]>>*/ abc /*<<[end]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_18(self):
            text = """/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*//*<<[ block2 ]>>*/ def /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_19(self):
            text = """/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*/\n/*<<[ block2 ]>>*/ def /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_20(self):
            # Block inside another block is considered part of the outer block
            text = """/*<<[ block1 ]>>*/ abc /*<<[ block2 ]>>*/ def /*<<[ end ]>>*/ /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_21(self):
            # Empty block name inside another block is not considered an error
            text = """/*<<[ block1 ]>>*/ abc /*<<[ ]>>*/ def /*<<[ end ]>>*/ /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_22(self):
            text = """\n\n<<[ block1 ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_23(self):
            text = """\n\n<<[ block1 ]>>  <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_24(self):
            text = """\n\n<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_25(self):
            text = """\n\n<<[ block1 ]>>    abc    <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_26(self):
            text = """\n\n<<[block1]>> abc <<[end]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_27(self):
            text = """\n\n<<[   block1   ]>> abc <<[end]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_28(self):
            text = """\n\n<<[ block1 ]>> abc <<[ end ]>><<[ block2 ]>> def <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_29(self):
            text = """\n\n<<[ block1 ]>> abc <<[ end ]>> <<[ block2 ]>> def <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_30(self):
            text = """\n\n<<[ block1 ]>> abc <<[ end ]>>\n<<[ block2 ]>> def <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_31(self):
            # Block inside another block is considered part of the outer block
            text = """\n\n<<[ block1 ]>> abc <<[ block2 ]>> def <<[ end ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_32(self):
            # Empty block name inside another block is not considered an error
            text = """\n\n<<[ block1 ]>> abc <<[ ]>> def <<[ end ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_33(self):
            text = """\n\n/*<<[ block1 ]>>*/ /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_34(self):
            text = """\n\n/*<<[ block1 ]>>*/  /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_35(self):
            text = """\n\n/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_36(self):
            text = """\n\n/*<<[ block1 ]>>*/    abc    /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_37(self):
            text = """\n\n/*<<[block1]>>*/ abc /*<<[end]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_38(self):
            text = """\n\n/*<<[   block1   ]>>*/ abc /*<<[end]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_39(self):
            text = """\n\n/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*//*<<[ block2 ]>>*/ def /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_40(self):
            text = """\n\n/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*/ /*<<[ block2 ]>>*/ def /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_41(self):
            text = """\n\n/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*/\n/*<<[ block2 ]>>*/ def /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_42(self):
            # Block inside another block is considered part of the outer block
            text = """\n\n/*<<[ block1 ]>>*/ abc /*<<[ block2 ]>>*/ def /*<<[ end ]>>*/ /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_43(self):
            # Empty block name inside another block is not considered an error
            text = """\n\n/*<<[ block1 ]>>*/ abc /*<<[ ]>>*/ def /*<<[ end ]>>*/ /*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_44(self):
            # Block with Python parameters
            text = """<<[ block1('string', 1, 1.0, ['a', 'b', 'c']) ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_45(self):
            # Block with Python parameters
            text = """<<[ block1("string", 1   , 1.0, [ 'a'  , 'b'   , 'c']) ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_46(self):
            # Block with Python parameters
            text = """<<[ block1("string", 1, 1.0000, ['a', 'b', 'c']) ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_47(self):
            # Block with Python parameters
            text = """<<[ block1("string", 1, 1.0000, ['a', param=[1, 2, 3], 'c']) ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_48(self):
            # Block with Python parameters
            text = """<<[ block1("string", 1, 1.0000, ['a', param=[1, 2, 3], {'a': 1, 'b': 2}]) ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_49(self):
            text = """/*<<[block1]>>*/\tabc\t/*<<[end]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_50(self):
            text = """/*<<[block1]>>*/\t\tabc\t\t/*<<[end]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_51(self):
            text = """abc def"""
            assert blockgen.string.has_blocks(text) == False

    class Test_Inline_ErrorCases:

        def test_1(self):
            text = """// <<[]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_2(self):
            text = """// <<[ ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_3(self):
            text = """// <<[ block1 ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_4(self):
            # Block inside another block is considered part of the outer block
            text = """// <<[ block1 ]>><<[ block2 ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_5(self):
            # Empty block name inside another block is not considered an error
            text = """// <<[ block1 ]>><<[ ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_6(self):
            text = """// <<[ block1 ]>><<[ block2 ]>><<[ ]>><<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_7(self):
            text = """// <<[ block1 ]>><<[ block2 ]>><<[ end ]>><<[ ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_8(self):
            text = """// <<[ block1 ]>><<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_9(self):
            text = """// <<[ block1 ]>><<[block2]>><<[end]>><<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_10(self):
            text = """// /*<<[]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_11(self):
            text = """// /*<<[ ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_12(self):
            text = """// /*<<[ block1 ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_13(self):
            # Block inside another block is considered part of the outer block
            text = """// /*<<[ block1 ]>>*//*<<[ block2 ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_14(self):
            # Empty block name inside another block is not considered an error
            text = """// /*<<[ block1 ]>>*//*<<[ ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_15(self):
            text = """// /*<<[ block1 ]>>*//*<<[ block2 ]>>*//*<<[ ]>>*//*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_16(self):
            text = """// /*<<[ block1 ]>>*//*<<[ block2 ]>>*//*<<[ end ]>>*//*<<[ ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_17(self):
            text = """// /*<<[ block1 ]>>*//*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_18(self):
            text = """// /*<<[ block1 ]>>*//*<<[block2]>>*//*<<[end]>>*//*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_19(self):
            text = """\n\n// <<[]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_20(self):
            text = """\n\n// <<[ ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_21(self):
            text = """\n\n// <<[ block1 ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_22(self):
            # Block inside another block is considered part of the outer block
            text = """\n\n// <<[ block1 ]>><<[ block2 ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_23(self):
            # Empty block name inside another block is not considered an error
            text = """\n\n// <<[ block1 ]>><<[ ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_24(self):
            text = """\n\n// <<[ block1 ]>><<[ block2 ]>><<[ ]>><<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_25(self):
            text = """\n\n// <<[ block1 ]>><<[ block2 ]>><<[ end ]>><<[ ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_26(self):
            text = """\n\n// <<[ block1 ]>><<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_27(self):
            text = """\n\n// <<[ block1 ]>><<[block2]>><<[end]>><<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_28(self):
            text = """\n\n// /*<<[]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_29(self):
            text = """\n\n// /*<<[ ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_30(self):
            text = """\n\n// /*<<[ block1 ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_31(self):
            # Block inside another block is considered part of the outer block
            text = """\n\n// /*<<[ block1 ]>>*//*<<[ block2 ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_32(self):
            # Empty block name inside another block is not considered an error
            text = """\n\n// /*<<[ block1 ]>>*//*<<[ ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_33(self):
            text = """\n\n// /*<<[ block1 ]>>*//*<<[ block2 ]>>*//*<<[ ]>>*//*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_34(self):
            text = """\n\n// /*<<[ block1 ]>>*//*<<[ block2 ]>>*//*<<[ end ]>>*//*<<[ ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_35(self):
            text = """\n\n// /*<<[ block1 ]>>*//*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_36(self):
            text = """\n\n// /*<<[ block1 ]>>*//*<<[block2]>>*//*<<[end]>>*//*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_37(self):
            text = """// <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_38(self):
            text = """\n\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_39(self):
            text = """<<[ block1 ]>> <<[ end ]>><<[ block1 ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_40(self):
            text = """/*<<[ block1 ]>>*//*<<[ end ]>>*//*<<[ block2 ]>>*//*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_41(self):
            text = """/*<<[ block1 ]>>*/ /*<<[ end ]>>*//*<<[ block2 ]>>*//*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_42(self):
            text = """<<[ 1block ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_43(self):
            text = """<<[ block1 block2 ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_44(self):
            text = """<<[ block1('a', '1')) ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_45(self):
            text = """<<[ block1(end_idx) ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_46(self):
            text = """<<[ 123 ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_47(self):
            text = """<<[ block(a=1, a=1) ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_48(self):
            text = """<<[ block(a=1, 2) ]>> <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

    class Test_Inline_Options:

        def test_1(self):
            try:
                os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"] = "((("
                text = """((( block1 ]>> abc ((( end ]>>"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>> abc <<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False
            finally:
                del os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"]

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_2(self):
            try:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL("(((")
                text = """((( block1 ]>> abc ((( end ]>>"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>> abc <<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False
            finally:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL(None)

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_3(self):
            blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL("<<[")
            with blockgen.options(open_marker_literal="((("):
                text = """((( block1 ]>> abc ((( end ]>>"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>> abc <<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_4(self):
            try:
                os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"] = ")))"
                text = """<<[ block1 ))) abc <<[ end )))"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>> abc <<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False
            finally:
                del os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"]

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_5(self):
            try:
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(")))")
                text = """<<[ block1 ))) abc <<[ end )))"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>> abc <<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False
            finally:
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(None)

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_6(self):
            blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL("]>>")
            with blockgen.options(close_marker_literal=")))"):
                text = """<<[ block1 ))) abc <<[ end )))"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>> abc <<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_7(self):
            try:
                os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"] = "@@@"
                text = """<<[ block1 ]>> abc <<[ @@@ ]>>"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>> abc <<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == True
            finally:
                del os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"]

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_8(self):
            try:
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION("@@@")
                text = """<<[ block1 ]>> abc <<[ @@@ ]>>"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>> abc <<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == True
            finally:
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION(None)

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_9(self):
            blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION(None)
            with blockgen.options(end_block_expression="@@@"):
                text = """<<[ block1 ]>> abc <<[ @@@ ]>>"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>> abc <<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == True

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_10(self):
            try:
                os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"] = "((("
                os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"] = ")))"
                os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"] = "@@@"
                text = """((( block1 ))) abc ((( @@@ )))"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>> abc <<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False
            finally:
                del os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"]
                del os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"]
                del os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"]

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_11(self):
            try:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL("(((")
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(")))")
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION("@@@")
                text = """((( block1 ))) abc ((( @@@ )))"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>> abc <<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False
            finally:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL(None)
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(None)
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION(None)

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_12(self):
            with blockgen.options(open_marker_literal="[[[",
                                  close_marker_literal="]]]",
                                  end_block_expression="&&&"):
                with blockgen.options(open_marker_literal="(((",
                                      close_marker_literal=")))",
                                      end_block_expression="@@@"):
                    text = """((( block1 ))) abc ((( @@@ )))"""
                    assert blockgen.string.has_blocks(text) == True
                    text = """<<[ block1 ]>> abc <<[ end ]>>"""
                    assert blockgen.string.has_blocks(text) == False

                text = """[[[ block1 ]]] abc [[[ &&& ]]]"""
                assert blockgen.string.has_blocks(text) == True

class Test_Multiline:

    class Test_Multiline_NominalCases:

        def test_1(self):
            text = """
                <<[ block1 ]>>
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_2(self):
            text = """
                <<[ block1 ]>>

                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_3(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_4(self):
            text = """
                <<[block1]>>
                abc
                <<[end]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_5(self):
            text = """
                <<[   block1   ]>>
                abc
                <<[end]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_6(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
                <<[ block2 ]>>
                def
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_7(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>><<[ block2 ]>>
                           def
                           <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_8(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>><<[ block2 ]>>
                           def
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_9(self):
            # Block inside another block is considered part of the outer block
            text = """
                <<[ block1 ]>>
                abc
                <<[ block2 ]>>
                def
                <<[ end ]>>
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_10(self):
            # Empty block name inside another block is not considered an error
            text = """
                <<[ block1 ]>>
                abc
                <<[ ]>>
                def
                <<[ end ]>>
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_11(self):
            text = """
                <<[ block1 ]>>
            abc
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_12(self):
            text = """
                <<[ block1 ]>>
              abc
                def
                  ghi
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_13(self):
            text = """
                <<[ block1 ]>>
              abc
                def
                  ghi
                <<[ end ]>><<[ block2 ]>>
                         123
                           456
                             789
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_14(self):
            text = """
                <<[ block1 ]>>
              abc
                def
                  ghi
                <<[ end ]>> <<[ block2 ]>>
                          123
                            456
                              789
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_15(self):
            text = """
                /*<<[ block1 ]>>*/
                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_16(self):
            text = """
                /*<<[ block1 ]>>*/

                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_17(self):
            text = """
                /*<<[ block1 ]>>*/
                abc
                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_18(self):
            text = """
                /*<<[block1]>>*/
                abc
                /*<<[end]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_19(self):
            text = """
                /*<<[   block1   ]>>*/
                abc
                /*<<[end]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_20(self):
            text = """
                /*<<[ block1 ]>>*/
                abc
                /*<<[ end ]>>*/
                /*<<[ block2 ]>>*/
                def
                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_21(self):
            text = """
                /*<<[ block1 ]>>*/
                abc
                /*<<[ end ]>>*//*<<[ block2 ]>>*/
                             def
                             /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_22(self):
            text = """
                /*<<[ block1 ]>>*/
                abc
                /*<<[ end ]>>*//*<<[ block2 ]>>*/
                             def
                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_23(self):
            # Block inside another block is considered part of the outer block
            text = """
                /*<<[ block1 ]>>*/
                abc
                /*<<[ block2 ]>>*/
                def
                /*<<[ end ]>>*/
                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_24(self):
            # Empty block name inside another block is not considered an error
            text = """
                /*<<[ block1 ]>>*/
                abc
                /*<<[ ]>>*/
                def
                /*<<[ end ]>>*/
                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_25(self):
            text = """
                /*<<[ block1 ]>>*/
            abc
                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_26(self):
            text = """
                /*<<[ block1 ]>>*/
              abc
                def
                  ghi
                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_27(self):
            text = """
                /*<<[ block1 ]>>*/
              abc
                def
                  ghi
                /*<<[ end ]>>*/<<[ block2 ]>>
                           123
                             456
                               789
                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_28(self):
            text = """
                /*<<[ block1 ]>>*/
              abc
                def
                  ghi
                /*<<[ end ]>>*/ <<[ block2 ]>>
                              123
                                456
                                  789
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_29(self):
            text = """
                /*<<[ block1 ]>>*/
              abc
                def
                  ghi
                /*<<[ end ]>>*/]>>*/ <<[ block2 ]>>
                                   123
                                     456
                                       789
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_30(self):
            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_31(self):
            text = """<<[ block1 ]>>abc\n\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_32(self):
            text = """<<[ block1 ]>>\n\nabc<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_33(self):
            text = """ <<[ block1 ]>>\nabc\n// <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_34(self):
            text = """// <<[ block1 ]>>\n     abc\n// <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_35(self):
            text = """ // <<[ block1 ]>>\n     abc\n// <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_36(self):
            text = """]>>// <<[ block1 ]>>\n       abc\n// <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_37(self):
            text = """]>>// <<[ block1 ]>>\nabc\n// <<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_38(self):
            text = """/*<<[ block1 ]>>*/\nabc\n/*<<[ end ]>>*//*<<[ block2 ]>>*/\ndef\n/*<<[ end ]>>*/"""
            assert blockgen.string.has_blocks(text) == True

        def test_39(self):
            text = """
                /*<<[ block1 ]>>*/
                abc
                /*<<[ end ]>>*/
                /*<<[ block2 ]>>*/
                def
                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_40(self):
            text = """
                /*<<[ block1(1, 2) ]>>*/
                abc
                /*<<[ end ]>>*/
                /*<<[ block2("1", "2") ]>>*/
                def
                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_41(self):
            text = """
                /*<<[ block1(1, p2=2) ]>>*/
                abc
                /*<<[ end ]>>*/
                /*<<[ block2("1", "2") ]>>*/
                def
                /*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_42(self):
            text = """
                /*<<[block1]>>*/
                \tabc\t
                /*<<[end]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_43(self):
            text = """
                \t/*<<[block1]>>*/
                \t\tabc\t
                \t/*<<[end]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_44(self):
            text = """
                /*<<[block1]>>*/
                \t\tabc\t
                /*<<[end]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_45(self):
            text = """
                <<[ block1 ]>> <<[ block2 ]>> def <<[ end ]>>
                abc
                <<[end]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_46(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ block2 ]>> def <<[ end ]>> <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_47(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>> <<[ block2 ]>> def <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_48(self):
            text = """
                /*<<[block1]>>*/
                \tabc\t
                /*<<[end]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_49(self):
            text = """
                /*<<[block1]>>*/
                \tabc\t
                /*<<[end]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_50(self):
            text = """
              \t/*<<[block1]>>*/
              \t\tabc\t
              \t/*<<[end]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_51(self):
            text = """
                /*<<[block1]>>*/
              \t\tabc\t
                /*<<[end]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_52(self):
            text = """
                <<[ block1 ]>> <<[ block2 ]>> def <<[ end ]>>
                abc
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_53(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ block2 ]>> def <<[ end ]>> <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_54(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>> <<[ block2 ]>> def <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_55(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>> <<[ block2 ]>> def <<[ end ]>> <<[ block3 ]>>
                ghi
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_56(self):
            text = """
                abc
                def
            """
            assert blockgen.string.has_blocks(text) == False

    class Test_Multiline_ErrorCases:

        def test_1(self):
            text = """
                // <<[]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_2(self):
            text = """
                // <<[ ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_3(self):
            text = """
                // <<[ block1 ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_4(self):
            # Block inside another block is considered part of the outer block
            text = """
                // <<[ block1 ]>><<[ block2 ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_5(self):
            # Empty block name inside another block is not considered an error
            text = """
                // <<[ block1 ]>><<[ ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_6(self):
            text = """
                // <<[ block1 ]>>
                       <<[ block2 ]>>
                           <<[ ]>><<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_7(self):
            text = """
                // <<[ block1 ]>>
                       <<[ block2 ]>>
                           <<[ end ]>>
                               <<[ ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_8(self):
            text = """
                // <<[ block1 ]>><<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_9(self):
            text = """
                // <<[ block1 ]>><<[block2]>><<[end]>><<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_10(self):
            text = """
                // /*<<[]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_11(self):
            text = """
                // /*<<[ ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_12(self):
            text = """
                // /*<<[ block1 ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_13(self):
            # Block inside another block is considered part of the outer block
            text = """
                // /*<<[ block1 ]>>*/
                       /*<<[ block2 ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_14(self):
            # Empty block name inside another block is not considered an error
            text = """
                // /*<<[ block1 ]>>*/
                       /*<<[ ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_15(self):
            text = """
                // /*<<[ block1 ]>>*/
                       /*<<[ block2 ]>>*/
                           /*<<[ ]>>*//*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_16(self):
            text = """
                // /*<<[ block1 ]>>*/
                       /*<<[ block2 ]>>*/
                           /*<<[ end ]>>*//*<<[ ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_17(self):
            text = """
                // /*<<[ block1 ]>>*//*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_18(self):
            text = """
                // /*<<[ block1 ]>>*//*<<[block2]>>*//*<<[end]>>*//*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_19(self):
            text = """
                \n\n// <<[]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_20(self):
            text = """
                \n\n// <<[ ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_21(self):
            text = """
                \n\n// <<[ block1 ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_22(self):
            # Block inside another block is considered part of the outer block
            text = """
                \n\n// <<[ block1 ]>>
                           <<[ block2 ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_23(self):
            # Empty block name inside another block is not considered an error
            text = """
                \n\n// <<[ block1 ]>>
                           <<[ ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_24(self):
            text = """
                \n\n// <<[ block1 ]>>
                           <<[ block2 ]>>
                               <<[ ]>><<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_25(self):
            text = """
                \n\n// <<[ block1 ]>>
                           <<[ block2 ]>>
                               <<[ end ]>><<[ ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_26(self):
            text = """
                \n\n// <<[ block1 ]>><<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_27(self):
            text = """
                \n\n// <<[ block1 ]>><<[block2]>><<[end]>><<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_28(self):
            text = """
                \n\n// /*<<[]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_29(self):
            text = """
                \n\n// /*<<[ ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_30(self):
            text = """
                \n\n// /*<<[ block1 ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_31(self):
            # Block inside another block is considered part of the outer block
            text = """
                \n\n// /*<<[ block1 ]>>*/
                           /*<<[ block2 ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_32(self):
            # Empty block name inside another block is not considered an error
            text = """
                \n\n// /*<<[ block1 ]>>*/
                           /*<<[ ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_33(self):
            text = """
                \n\n// /*<<[ block1 ]>>*/
                           /*<<[ block2 ]>>*/
                               /*<<[ ]>>*//*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_34(self):
            text = """
                \n\n// /*<<[ block1 ]>>*/
                           /*<<[ block2 ]>>*/
                               /*<<[ end ]>>*//*<<[ ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_35(self):
            text = """
                \n\n// /*<<[ block1 ]>>*//*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_36(self):
            text = """
                \n\n// /*<<[ block1 ]>>*//*<<[block2]>>*//*<<[end]>>*//*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_37(self):
            text = """
                // <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_38(self):
            text = """
                \n\n<<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_39(self):
            text = """
                <<[ block1 ]>>
                <<[ end ]>>
                <<[ block1 ]>>
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_40(self):
            text = """
                /*<<[ block1 ]>>*//*<<[ end ]>>*/
                /*<<[ block2 ]>>*//*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_41(self):
            text = """
                /*<<[ block1 ]>>*/ /*<<[ end ]>>*/
                /*<<[ block2 ]>>*//*<<[ end ]>>*/
            """
            assert blockgen.string.has_blocks(text) == True

        def test_42(self):
            text = """
                <<[ 1block ]>>
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_43(self):
            text = """
                <<[ block1 block2 ]>>
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_44(self):
            text = """
                <<[ block1('a', '1')) ]>>
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_45(self):
            text = """
                <<[ block1(end_idx) ]>>
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_46(self):
            text = """
                <<[ 123 ]>>
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_47(self):
            text = """
                <<[ block(a=1, a=1) ]>>
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

        def test_48(self):
            text = """
                <<[ block(a=1, 2) ]>>
                <<[ end ]>>
            """
            assert blockgen.string.has_blocks(text) == True

    class Test_Multiline_Options:

        def test_1(self):
            try:
                os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"] = "((("
                text = """((( block1 ]>>\nabc\n((( end ]>>"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False
            finally:
                del os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"]

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_2(self):
            try:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL("(((")
                text = """((( block1 ]>>\nabc\n((( end ]>>"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False
            finally:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL(None)

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_3(self):
            blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL("<<[")
            with blockgen.options(open_marker_literal="((("):
                text = """((( block1 ]>>\nabc\n((( end ]>>"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_4(self):
            try:
                os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"] = ")))"
                text = """<<[ block1 )))\nabc\n<<[ end )))"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False
            finally:
                del os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"]

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_5(self):
            try:
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(")))")
                text = """<<[ block1 )))\nabc\n<<[ end )))"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False
            finally:
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(None)

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_6(self):
            blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL("]>>")
            with blockgen.options(close_marker_literal=")))"):
                text = """<<[ block1 )))\nabc\n<<[ end )))"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_7(self):
            try:
                os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"] = "@@@"
                text = """<<[ block1 ]>>\nabc\n<<[ @@@ ]>>"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == True
            finally:
                del os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"]

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_8(self):
            try:
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION("@@@")
                text = """<<[ block1 ]>>\nabc\n<<[ @@@ ]>>"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == True
            finally:
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION(None)

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_9(self):
            blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION("end")
            with blockgen.options(end_block_expression="@@@"):
                text = """<<[ block1 ]>>\nabc\n<<[ @@@ ]>>"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == True

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_10(self):
            try:
                os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"] = "((("
                os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"] = ")))"
                os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"] = "@@@"
                text = """((( block1 )))\nabc\n((( @@@ )))"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False
            finally:
                del os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"]
                del os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"]
                del os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"]

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_11(self):
            try:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL("(((")
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(")))")
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION("@@@")
                text = """((( block1 )))\nabc\n((( @@@ )))"""
                assert blockgen.string.has_blocks(text) == True
                text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
                assert blockgen.string.has_blocks(text) == False
            finally:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL(None)
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(None)
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION(None)

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            assert blockgen.string.has_blocks(text) == True

        def test_12(self):
            with blockgen.options(open_marker_literal="[[[",
                                  close_marker_literal="]]]",
                                  end_block_expression="&&&"):
                with blockgen.options(open_marker_literal="(((",
                                      close_marker_literal=")))",
                                      end_block_expression="@@@"):
                    text = """((( block1 )))\nabc\n((( @@@ )))"""
                    assert blockgen.string.has_blocks(text) == True
                    text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
                    assert blockgen.string.has_blocks(text) == False

                text = """[[[ block1 ]]]\nabc\n[[[ &&& ]]]"""
                assert blockgen.string.has_blocks(text) == True
