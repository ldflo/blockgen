import blockgen
import os
import sys

class Test_Inline:

    class Test_Inline_NominalCases:

        def test_1(self):
            text = """<<[ block1 ]>> <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """"""

        def test_2(self):
            text = """<<[ block1 ]>>   <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """ """

        def test_3(self):
            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_4(self):
            text = """<<[ block1 ]>>    abc    <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """   abc   """

        def test_5(self):
            text = """<<[block1]>> abc <<[end]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_6(self):
            text = """<<[   block1   ]>> abc <<[end]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_7(self):
            text = """<<[ block1 ]>> abc <<[ end ]>><<[ block2 ]>> def <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abcdef"""

        def test_8(self):
            text = """<<[ block1 ]>> abc <<[ end ]>> <<[ block2 ]>> def <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc def"""

        def test_9(self):
            text = """<<[ block1 ]>> abc <<[ end ]>>\n<<[ block2 ]>> def <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc\ndef"""

        def test_10(self):
            # Block inside another block is considered part of the outer block
            text = """<<[ block1 ]>> abc <<[ block2 ]>> def <<[ end ]>> <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc <<[ block2 ]>> def <<[ end ]>>"""

        def test_11(self):
            # Empty block name inside another block is not considered an error
            text = """<<[ block1 ]>> abc <<[ ]>> def <<[ end ]>> <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc <<[ ]>> def <<[ end ]>>"""

        def test_12(self):
            text = """/*<<[ block1 ]>>*/ /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """"""

        def test_13(self):
            text = """/*<<[ block1 ]>>*/  /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """"""

        def test_14(self):
            text = """/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_15(self):
            text = """/*<<[ block1 ]>>*/    abc    /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """   abc   """

        def test_16(self):
            text = """/*<<[block1]>>*/ abc /*<<[end]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_17(self):
            text = """/*<<[   block1   ]>>*/ abc /*<<[end]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_18(self):
            text = """/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*//*<<[ block2 ]>>*/ def /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abcdef"""

        def test_19(self):
            text = """/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*/\n/*<<[ block2 ]>>*/ def /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc\ndef"""

        def test_20(self):
            # Block inside another block is considered part of the outer block
            text = """/*<<[ block1 ]>>*/ abc /*<<[ block2 ]>>*/ def /*<<[ end ]>>*/ /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc /*<<[ block2 ]>>*/ def /*<<[ end ]>>*/"""

        def test_21(self):
            # Empty block name inside another block is not considered an error
            text = """/*<<[ block1 ]>>*/ abc /*<<[ ]>>*/ def /*<<[ end ]>>*/ /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc /*<<[ ]>>*/ def /*<<[ end ]>>*/"""

        def test_22(self):
            text = """\n\n<<[ block1 ]>> <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\n"""

        def test_23(self):
            text = """\n\n<<[ block1 ]>>  <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\n"""

        def test_24(self):
            text = """\n\n<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc"""

        def test_25(self):
            text = """\n\n<<[ block1 ]>>    abc    <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\n   abc   """

        def test_26(self):
            text = """\n\n<<[block1]>> abc <<[end]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc"""

        def test_27(self):
            text = """\n\n<<[   block1   ]>> abc <<[end]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc"""

        def test_28(self):
            text = """\n\n<<[ block1 ]>> abc <<[ end ]>><<[ block2 ]>> def <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabcdef"""

        def test_29(self):
            text = """\n\n<<[ block1 ]>> abc <<[ end ]>> <<[ block2 ]>> def <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc def"""

        def test_30(self):
            text = """\n\n<<[ block1 ]>> abc <<[ end ]>>\n<<[ block2 ]>> def <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc\ndef"""

        def test_31(self):
            # Block inside another block is considered part of the outer block
            text = """\n\n<<[ block1 ]>> abc <<[ block2 ]>> def <<[ end ]>> <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc <<[ block2 ]>> def <<[ end ]>>"""

        def test_32(self):
            # Empty block name inside another block is not considered an error
            text = """\n\n<<[ block1 ]>> abc <<[ ]>> def <<[ end ]>> <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc <<[ ]>> def <<[ end ]>>"""

        def test_33(self):
            text = """\n\n/*<<[ block1 ]>>*/ /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\n"""

        def test_34(self):
            text = """\n\n/*<<[ block1 ]>>*/  /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\n"""

        def test_35(self):
            text = """\n\n/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc"""

        def test_36(self):
            text = """\n\n/*<<[ block1 ]>>*/    abc    /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\n   abc   """

        def test_37(self):
            text = """\n\n/*<<[block1]>>*/ abc /*<<[end]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc"""

        def test_38(self):
            text = """\n\n/*<<[   block1   ]>>*/ abc /*<<[end]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc"""

        def test_39(self):
            text = """\n\n/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*//*<<[ block2 ]>>*/ def /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabcdef"""

        def test_40(self):
            text = """\n\n/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*/ /*<<[ block2 ]>>*/ def /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc def"""

        def test_41(self):
            text = """\n\n/*<<[ block1 ]>>*/ abc /*<<[ end ]>>*/\n/*<<[ block2 ]>>*/ def /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc\ndef"""

        def test_42(self):
            # Block inside another block is considered part of the outer block
            text = """\n\n/*<<[ block1 ]>>*/ abc /*<<[ block2 ]>>*/ def /*<<[ end ]>>*/ /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc /*<<[ block2 ]>>*/ def /*<<[ end ]>>*/"""

        def test_43(self):
            # Empty block name inside another block is not considered an error
            text = """\n\n/*<<[ block1 ]>>*/ abc /*<<[ ]>>*/ def /*<<[ end ]>>*/ /*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n\nabc /*<<[ ]>>*/ def /*<<[ end ]>>*/"""

        def test_44(self):
            # Block with Python parameters
            text = """<<[ block1('string', 1, 1.0, ['a', 'b', 'c']) ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_45(self):
            # Block with Python parameters
            text = """<<[ block1("string", 1   , 1.0, [ 'a'  , 'b'   , 'c']) ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_46(self):
            # Block with Python parameters
            text = """<<[ block1("string", 1, 1.0000, ['a', 'b', 'c']) ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_47(self):
            # Block with Python parameters
            text = """<<[ block1("string", 1, 1.0000, ['a', [1, 2, 3], 'c']) ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_48(self):
            # Block with Python parameters
            text = """<<[ block1("string", 1, 1.0000, ['a', [1, 2, 3], {'a': 1, 'b': 2}]) ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_49(self):
            text = """/*<<[block1]>>*/\tabc\t/*<<[end]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\tabc\t"""

        def test_50(self):
            text = """/*<<[block1]>>*/\t\tabc\t\t/*<<[end]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\t\tabc\t\t"""

    class Test_Inline_ErrorCases:

        def test_1(self):
            text = """// <<[]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[]>>' at line 1, column 4"
            except Exception:
                raise

        def test_2(self):
            text = """// <<[ ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[ ]>>' at line 1, column 4"
            except Exception:
                raise

        def test_3(self):
            text = """// <<[ block1 ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 1, column 4"
            except Exception:
                raise

        def test_4(self):
            # Block inside another block is considered part of the outer block
            text = """// <<[ block1 ]>><<[ block2 ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 1, column 4"
            except Exception:
                raise

        def test_5(self):
            # Empty block name inside another block is not considered an error
            text = """// <<[ block1 ]>><<[ ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 1, column 4"
            except Exception:
                raise

        def test_6(self):
            text = """// <<[ block1 ]>><<[ block2 ]>><<[ ]>><<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 1, column 4"
            except Exception:
                raise

        def test_7(self):
            text = """// <<[ block1 ]>><<[ block2 ]>><<[ end ]>><<[ ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 1, column 4"
            except Exception:
                raise

        def test_8(self):
            text = """// <<[ block1 ]>><<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '<<[ block1 ]>><<[ end ]>>' at line 1, column 4" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_9(self):
            text = """// <<[ block1 ]>><<[block2]>><<[end]>><<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '<<[ block1 ]>><<[block2]>><<[end]>><<[ end ]>>' at line 1, column 4" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_10(self):
            text = """// /*<<[]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[]>>' at line 1, column 6"
            except Exception:
                raise

        def test_11(self):
            text = """// /*<<[ ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[ ]>>' at line 1, column 6"
            except Exception:
                raise

        def test_12(self):
            text = """// /*<<[ block1 ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 1, column 6"
            except Exception:
                raise

        def test_13(self):
            # Block inside another block is considered part of the outer block
            text = """// /*<<[ block1 ]>>*//*<<[ block2 ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 1, column 6"
            except Exception:
                raise

        def test_14(self):
            # Empty block name inside another block is not considered an error
            text = """// /*<<[ block1 ]>>*//*<<[ ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 1, column 6"
            except Exception:
                raise

        def test_15(self):
            text = """// /*<<[ block1 ]>>*//*<<[ block2 ]>>*//*<<[ ]>>*//*<<[ end ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 1, column 6"
            except Exception:
                raise

        def test_16(self):
            text = """// /*<<[ block1 ]>>*//*<<[ block2 ]>>*//*<<[ end ]>>*//*<<[ ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 1, column 6"
            except Exception:
                raise

        def test_17(self):
            text = """// /*<<[ block1 ]>>*//*<<[ end ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '/*<<[ block1 ]>>*//*<<[ end ]>>*/' at line 1, column 6" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_18(self):
            text = """// /*<<[ block1 ]>>*//*<<[block2]>>*//*<<[end]>>*//*<<[ end ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '/*<<[ block1 ]>>*//*<<[block2]>>*//*<<[end]>>*//*<<[ end ]>>*/' at line 1, column 6" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_19(self):
            text = """\n\n// <<[]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[]>>' at line 3, column 4"
            except Exception:
                raise

        def test_20(self):
            text = """\n\n// <<[ ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[ ]>>' at line 3, column 4"
            except Exception:
                raise

        def test_21(self):
            text = """\n\n// <<[ block1 ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 3, column 4"
            except Exception:
                raise

        def test_22(self):
            # Block inside another block is considered part of the outer block
            text = """\n\n// <<[ block1 ]>><<[ block2 ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 3, column 4"
            except Exception:
                raise

        def test_23(self):
            # Empty block name inside another block is not considered an error
            text = """\n\n// <<[ block1 ]>><<[ ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 3, column 4"
            except Exception:
                raise

        def test_24(self):
            text = """\n\n// <<[ block1 ]>><<[ block2 ]>><<[ ]>><<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 3, column 4"
            except Exception:
                raise

        def test_25(self):
            text = """\n\n// <<[ block1 ]>><<[ block2 ]>><<[ end ]>><<[ ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 3, column 4"
            except Exception:
                raise

        def test_26(self):
            text = """\n\n// <<[ block1 ]>><<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '<<[ block1 ]>><<[ end ]>>' at line 3, column 4" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_27(self):
            text = """\n\n// <<[ block1 ]>><<[block2]>><<[end]>><<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '<<[ block1 ]>><<[block2]>><<[end]>><<[ end ]>>' at line 3, column 4" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_28(self):
            text = """\n\n// /*<<[]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[]>>' at line 3, column 6"
            except Exception:
                raise

        def test_29(self):
            text = """\n\n// /*<<[ ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[ ]>>' at line 3, column 6"
            except Exception:
                raise

        def test_30(self):
            text = """\n\n// /*<<[ block1 ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 3, column 6"
            except Exception:
                raise

        def test_31(self):
            # Block inside another block is considered part of the outer block
            text = """\n\n// /*<<[ block1 ]>>*//*<<[ block2 ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 3, column 6"
            except Exception:
                raise

        def test_32(self):
            # Empty block name inside another block is not considered an error
            text = """\n\n// /*<<[ block1 ]>>*//*<<[ ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 3, column 6"
            except Exception:
                raise

        def test_33(self):
            text = """\n\n// /*<<[ block1 ]>>*//*<<[ block2 ]>>*//*<<[ ]>>*//*<<[ end ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 3, column 6"
            except Exception:
                raise

        def test_34(self):
            text = """\n\n// /*<<[ block1 ]>>*//*<<[ block2 ]>>*//*<<[ end ]>>*//*<<[ ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 3, column 6"
            except Exception:
                raise

        def test_35(self):
            text = """\n\n// /*<<[ block1 ]>>*//*<<[ end ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '/*<<[ block1 ]>>*//*<<[ end ]>>*/' at line 3, column 6" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_36(self):
            text = """\n\n// /*<<[ block1 ]>>*//*<<[block2]>>*//*<<[end]>>*//*<<[ end ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '/*<<[ block1 ]>>*//*<<[block2]>>*//*<<[end]>>*//*<<[ end ]>>*/' at line 3, column 6" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_37(self):
            text = """// <<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.UnmatchedBlockEndMarkerError as e:
                assert str(e) == "Unmatched block end marker '<<[ end ]>>' at line 1, column 4"
            except Exception:
                raise

        def test_38(self):
            text = """\n\n<<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.UnmatchedBlockEndMarkerError as e:
                assert str(e) == "Unmatched block end marker '<<[ end ]>>' at line 3, column 1"
            except Exception:
                raise

        def test_39(self):
            text = """<<[ block1 ]>> <<[ end ]>><<[ block1 ]>> <<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.DuplicatedBlockExpressionError as e:
                assert str(e) == "Duplicated block '<<[ block1 ]>>' with same expression 'block1' at line 1, column 27"
            except Exception:
                raise

        def test_40(self):
            text = """/*<<[ block1 ]>>*//*<<[ end ]>>*//*<<[ block2 ]>>*//*<<[ end ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '/*<<[ block1 ]>>*//*<<[ end ]>>*//*' at line 1, column 3" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_41(self):
            text = """/*<<[ block1 ]>>*/ /*<<[ end ]>>*//*<<[ block2 ]>>*//*<<[ end ]>>*/"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '*//*<<[ block2 ]>>*//*<<[ end ]>>*/' at line 1, column 37" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_42(self):
            text = """<<[ 1block ]>> <<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ 1block ]>>' at line 1, column 1:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                if sys.version_info >= (3, 10):
                    assert str(e.__cause__) == "invalid decimal literal (<unknown>, line 1)"
                else:
                    assert str(e.__cause__) == "unexpected EOF while parsing (<unknown>, line 1)"
            except Exception:
                raise

        def test_43(self):
            text = """<<[ block1 block2 ]>> <<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ block1 block2 ]>>' at line 1, column 1:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                if sys.version_info >= (3, 10):
                    assert str(e.__cause__) == "invalid syntax (<unknown>, line 1)"
                else:
                    assert str(e.__cause__) == "unexpected EOF while parsing (<unknown>, line 1)"
            except Exception:
                raise

        def test_44(self):
            text = """<<[ block1('a', '1')) ]>> <<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ block1('a', '1')) ]>>' at line 1, column 1:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                assert str(e.__cause__) == "unmatched ')' (<unknown>, line 1)"
            except Exception:
                raise

        def test_45(self):
            text = """<<[ block1(end_idx) ]>> <<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ block1(end_idx) ]>>' at line 1, column 1:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                if sys.version_info >= (3, 14):
                    assert str(e.__cause__) == "malformed node or string on line 1: Name(id='end_idx', ctx=Load())"
                elif sys.version_info >= (3, 10):
                    assert str(e.__cause__).startswith("malformed node or string on line 1: <ast.Name object at")
                else:
                    assert str(e.__cause__).startswith("malformed node or string: <ast.Name object at")
            except Exception:
                raise

        def test_46(self):
            text = """<<[ 123 ]>> <<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ 123 ]>>' at line 1, column 1:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                assert str(e.__cause__) == "unexpected type '<class 'ast.Constant'>' for expression: 123"
            except Exception:
                raise

        def test_47(self):
            text = """<<[ block(a=1, a=1) ]>> <<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ block(a=1, a=1) ]>>' at line 1, column 1:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                assert str(e.__cause__) == "keyword argument repeated: a"
            except Exception:
                raise

        def test_48(self):
            text = """<<[ block(a=1, 2) ]>> <<[ end ]>>"""
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ block(a=1, 2) ]>>' at line 1, column 1:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                assert str(e.__cause__) == "positional argument follows keyword argument (<unknown>, line 1)"
            except Exception:
                raise

    class Test_Inline_Options:

        def test_1(self):
            try:
                os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"] = "((("
                text = """((( block1 ]>> abc ((( end ]>>"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == """abc"""
            finally:
                del os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"]

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_2(self):
            try:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL("(((")
                text = """((( block1 ]>> abc ((( end ]>>"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == """abc"""
            finally:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL(None)

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_3(self):
            blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL("<<[")
            with blockgen.options(open_marker_literal="((("):
                text = """((( block1 ]>> abc ((( end ]>>"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == """abc"""

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_4(self):
            try:
                os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"] = ")))"
                text = """<<[ block1 ))) abc <<[ end )))"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == """abc"""
            finally:
                del os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"]

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_5(self):
            try:
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(")))")
                text = """<<[ block1 ))) abc <<[ end )))"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == """abc"""
            finally:
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(None)

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_6(self):
            blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL("]>>")
            with blockgen.options(close_marker_literal=")))"):
                text = """<<[ block1 ))) abc <<[ end )))"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == """abc"""

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_7(self):
            try:
                os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"] = "@@@"
                text = """<<[ block1 ]>> abc <<[ @@@ ]>>"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == """abc"""
            finally:
                del os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"]

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_8(self):
            try:
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION("@@@")
                text = """<<[ block1 ]>> abc <<[ @@@ ]>>"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == """abc"""
            finally:
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION(None)

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_9(self):
            blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION("end")
            with blockgen.options(end_block_expression="@@@"):
                text = """<<[ block1 ]>> abc <<[ @@@ ]>>"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == """abc"""

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_10(self):
            try:
                os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"] = "((("
                os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"] = ")))"
                os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"] = "@@@"
                text = """((( block1 ))) abc ((( @@@ )))"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == """abc"""
            finally:
                del os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"]
                del os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"]
                del os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"]

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_11(self):
            try:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL("(((")
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(")))")
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION("@@@")
                text = """((( block1 ))) abc ((( @@@ )))"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == """abc"""
            finally:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL(None)
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(None)
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION(None)

            text = """<<[ block1 ]>> abc <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc"""

        def test_12(self):
            with blockgen.options(open_marker_literal="[[[",
                                  close_marker_literal="]]]",
                                  end_block_expression="&&&"):
                with blockgen.options(open_marker_literal="(((",
                                      close_marker_literal=")))",
                                      end_block_expression="@@@"):
                    text = """((( block1 ))) abc ((( @@@ )))"""
                    new_text = blockgen.string.remove_markers(text)
                    assert new_text == """abc"""

                text = """[[[ block1 ]]] abc [[[ &&& ]]]"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == """abc"""

class Test_Multiline:

    class Test_Multiline_NominalCases:

        def test_1(self):
            text = """
                <<[ block1 ]>>
                <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
            """

        def test_2(self):
            text = """
                <<[ block1 ]>>

                <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """

            """

        def test_3(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
            """

        def test_4(self):
            text = """
                <<[block1]>>
                abc
                <<[end]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
            """

        def test_5(self):
            text = """
                <<[   block1   ]>>
                abc
                <<[end]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
            """

        def test_6(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>>
                <<[ block2 ]>>
                def
                <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                def
            """

        def test_7(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>><<[ block2 ]>>
                           def
                           <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                           def
            """

        def test_8(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>><<[ block2 ]>>
                           def
                <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                           def
            """

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
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                <<[ block2 ]>>
                def
                <<[ end ]>>
            """

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
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                <<[ ]>>
                def
                <<[ end ]>>
            """

        def test_11(self):
            text = """
                <<[ block1 ]>>
            abc
                <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
            abc
            """

        def test_12(self):
            text = """
                <<[ block1 ]>>
              abc
                def
                  ghi
                <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
              abc
                def
                  ghi
            """

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
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
              abc
                def
                  ghi
                         123
                           456
                             789
            """

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
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
              abc
                def
                  ghi
                          123
                            456
                              789
            """

        def test_15(self):
            text = """
                /*<<[ block1 ]>>*/
                /*<<[ end ]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
            """

        def test_16(self):
            text = """
                /*<<[ block1 ]>>*/

                /*<<[ end ]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """

            """

        def test_17(self):
            text = """
                /*<<[ block1 ]>>*/
                abc
                /*<<[ end ]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
            """

        def test_18(self):
            text = """
                /*<<[block1]>>*/
                abc
                /*<<[end]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
            """

        def test_19(self):
            text = """
                /*<<[   block1   ]>>*/
                abc
                /*<<[end]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
            """

        def test_20(self):
            text = """
                /*<<[ block1 ]>>*/
                abc
                /*<<[ end ]>>*/
                /*<<[ block2 ]>>*/
                def
                /*<<[ end ]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                def
            """

        def test_21(self):
            text = """
                /*<<[ block1 ]>>*/
                abc
                /*<<[ end ]>>*//*<<[ block2 ]>>*/
                             def
                             /*<<[ end ]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                             def
            """

        def test_22(self):
            text = """
                /*<<[ block1 ]>>*/
                abc
                /*<<[ end ]>>*//*<<[ block2 ]>>*/
                             def
                /*<<[ end ]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                             def
            """

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
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                /*<<[ block2 ]>>*/
                def
                /*<<[ end ]>>*/
            """

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
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                /*<<[ ]>>*/
                def
                /*<<[ end ]>>*/
            """

        def test_25(self):
            text = """
                /*<<[ block1 ]>>*/
            abc
                /*<<[ end ]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
            abc
            """

        def test_26(self):
            text = """
                /*<<[ block1 ]>>*/
              abc
                def
                  ghi
                /*<<[ end ]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
              abc
                def
                  ghi
            """

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
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
              abc
                def
                  ghi
                           123
                             456
                               789
            """

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
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
              abc
                def
                  ghi
                              123
                                456
                                  789
            """

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
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
              abc
                def
                  ghi
                                   123
                                     456
                                       789
            """

        def test_30(self):
            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc\n"""

        def test_31(self):
            text = """<<[ block1 ]>>abc\n\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n"""

        def test_32(self):
            text = """<<[ block1 ]>>\n\nabc<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """\n"""

        def test_33(self):
            text = """ <<[ block1 ]>>\nabc\n// <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc\n"""

        def test_34(self):
            text = """// <<[ block1 ]>>\n     abc\n// <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """     abc\n"""

        def test_35(self):
            text = """ // <<[ block1 ]>>\n     abc\n// <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """     abc\n"""

        def test_36(self):
            text = """]>>// <<[ block1 ]>>\n       abc\n// <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """       abc\n"""

        def test_37(self):
            text = """]>>// <<[ block1 ]>>\nabc\n// <<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc\n"""

        def test_38(self):
            text = """/*<<[ block1 ]>>*/\nabc\n/*<<[ end ]>>*//*<<[ block2 ]>>*/\ndef\n/*<<[ end ]>>*/"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """abc\ndef\n"""

        def test_39(self):
            text = """
                /*<<[ block1 ]>>*/
                abc
                /*<<[ end ]>>*/
                /*<<[ block2 ]>>*/
                def
                /*<<[ end ]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                def
            """

        def test_40(self):
            text = """
                /*<<[ block1(1, 2) ]>>*/
                abc
                /*<<[ end ]>>*/
                /*<<[ block2("1", "2") ]>>*/
                def
                /*<<[ end ]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                def
            """

        def test_41(self):
            text = """
                /*<<[ block1(1, p2=2) ]>>*/
                abc
                /*<<[ end ]>>*/
                /*<<[ block2("1", "2") ]>>*/
                def
                /*<<[ end ]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                def
            """

        def test_42(self):
            text = """
                /*<<[block1]>>*/
                \tabc\t
                /*<<[end]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                \tabc\t
            """

        def test_43(self):
            text = """
                \t/*<<[block1]>>*/
                \t\tabc\t
                \t/*<<[end]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                \t\tabc\t
            """

        def test_44(self):
            text = """
                /*<<[block1]>>*/
                \t\tabc\t
                /*<<[end]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                \t\tabc\t
            """

        def test_45(self):
            text = """
                <<[ block1 ]>> <<[ block2 ]>> def <<[ end ]>>
                abc
                <<[end]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
            """

        def test_46(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ block2 ]>> def <<[ end ]>> <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
            """

        def test_47(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>> <<[ block2 ]>> def <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                def
            """

        def test_48(self):
            text = """
                /*<<[block1]>>*/
                \tabc\t
                /*<<[end]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                \tabc\t
            """

        def test_49(self):
            text = """
                /*<<[block1]>>*/
                \tabc\t
                /*<<[end]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                \tabc\t
            """

        def test_50(self):
            text = """
              \t/*<<[block1]>>*/
              \t\tabc\t
              \t/*<<[end]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
              \t\tabc\t
            """

        def test_51(self):
            text = """
                /*<<[block1]>>*/
              \t\tabc\t
                /*<<[end]>>*/
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
              \t\tabc\t
            """

        def test_52(self):
            text = """
                <<[ block1 ]>> <<[ block2 ]>> def <<[ end ]>>
                abc
                <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
            """

        def test_53(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ block2 ]>> def <<[ end ]>> <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
            """

        def test_54(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>> <<[ block2 ]>> def <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                def
            """

        def test_55(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>> <<[ block2 ]>> def <<[ end ]>> <<[ block3 ]>>
                ghi
                <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                def
                ghi
            """

        def test_56(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>> <<[ block2 ]>> def <<[ end ]>> <<[ block3 ]>> ghi <<[ end ]>> <<[ block4 ]>>
                123
                <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                def ghi
                123
            """

        def test_57(self):
            text = """
                <<[ block1 ]>>
                abc
                <<[ end ]>> ]>> <<[ block3 ]>>
                ghi
                <<[ end ]>>
            """
            new_text = blockgen.string.remove_markers(text)
            assert new_text == """
                abc
                ghi
            """

    class Test_Multiline_ErrorCases:

        def test_1(self):
            text = """
                // <<[]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[]>>' at line 2, column 20"
            except Exception:
                raise

        def test_2(self):
            text = """
                // <<[ ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[ ]>>' at line 2, column 20"
            except Exception:
                raise

        def test_3(self):
            text = """
                // <<[ block1 ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 2, column 20"
            except Exception:
                raise

        def test_4(self):
            # Block inside another block is considered part of the outer block
            text = """
                // <<[ block1 ]>><<[ block2 ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 2, column 20"
            except Exception:
                raise

        def test_5(self):
            # Empty block name inside another block is not considered an error
            text = """
                // <<[ block1 ]>><<[ ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 2, column 20"
            except Exception:
                raise

        def test_6(self):
            text = """
                // <<[ block1 ]>>
                       <<[ block2 ]>>
                           <<[ ]>><<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 2, column 20"
            except Exception:
                raise

        def test_7(self):
            text = """
                // <<[ block1 ]>>
                       <<[ block2 ]>>
                           <<[ end ]>>
                               <<[ ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 2, column 20"
            except Exception:
                raise

        def test_8(self):
            text = """
                // <<[ block1 ]>><<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '<<[ block1 ]>><<[ end ]>>' at line 2, column 20" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_9(self):
            text = """
                // <<[ block1 ]>><<[block2]>><<[end]>><<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '<<[ block1 ]>><<[block2]>><<[end]>><<[ end ]>>' at line 2, column 20" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_10(self):
            text = """
                // /*<<[]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[]>>' at line 2, column 22"
            except Exception:
                raise

        def test_11(self):
            text = """
                // /*<<[ ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[ ]>>' at line 2, column 22"
            except Exception:
                raise

        def test_12(self):
            text = """
                // /*<<[ block1 ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 2, column 22"
            except Exception:
                raise

        def test_13(self):
            # Block inside another block is considered part of the outer block
            text = """
                // /*<<[ block1 ]>>*/
                       /*<<[ block2 ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 2, column 22"
            except Exception:
                raise

        def test_14(self):
            # Empty block name inside another block is not considered an error
            text = """
                // /*<<[ block1 ]>>*/
                       /*<<[ ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 2, column 22"
            except Exception:
                raise

        def test_15(self):
            text = """
                // /*<<[ block1 ]>>*/
                       /*<<[ block2 ]>>*/
                           /*<<[ ]>>*//*<<[ end ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 2, column 22"
            except Exception:
                raise

        def test_16(self):
            text = """
                // /*<<[ block1 ]>>*/
                       /*<<[ block2 ]>>*/
                           /*<<[ end ]>>*//*<<[ ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 2, column 22"
            except Exception:
                raise

        def test_17(self):
            text = """
                // /*<<[ block1 ]>>*//*<<[ end ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '/*<<[ block1 ]>>*//*<<[ end ]>>*/' at line 2, column 22" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_18(self):
            text = """
                // /*<<[ block1 ]>>*//*<<[block2]>>*//*<<[end]>>*//*<<[ end ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '/*<<[ block1 ]>>*//*<<[block2]>>*//*<<[end]>>*//*<<[ end ]>>*/' at line 2, column 22" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_19(self):
            text = """
                \n\n// <<[]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[]>>' at line 4, column 4"
            except Exception:
                raise

        def test_20(self):
            text = """
                \n\n// <<[ ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[ ]>>' at line 4, column 4"
            except Exception:
                raise

        def test_21(self):
            text = """
                \n\n// <<[ block1 ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 4, column 4"
            except Exception:
                raise

        def test_22(self):
            # Block inside another block is considered part of the outer block
            text = """
                \n\n// <<[ block1 ]>>
                           <<[ block2 ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 4, column 4"
            except Exception:
                raise

        def test_23(self):
            # Empty block name inside another block is not considered an error
            text = """
                \n\n// <<[ block1 ]>>
                           <<[ ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 4, column 4"
            except Exception:
                raise

        def test_24(self):
            text = """
                \n\n// <<[ block1 ]>>
                           <<[ block2 ]>>
                               <<[ ]>><<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 4, column 4"
            except Exception:
                raise

        def test_25(self):
            text = """
                \n\n// <<[ block1 ]>>
                           <<[ block2 ]>>
                               <<[ end ]>><<[ ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 4, column 4"
            except Exception:
                raise

        def test_26(self):
            text = """
                \n\n// <<[ block1 ]>><<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '<<[ block1 ]>><<[ end ]>>' at line 4, column 4" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_27(self):
            text = """
                \n\n// <<[ block1 ]>><<[block2]>><<[end]>><<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '<<[ block1 ]>><<[block2]>><<[end]>><<[ end ]>>' at line 4, column 4" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_28(self):
            text = """
                \n\n// /*<<[]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[]>>' at line 4, column 6"
            except Exception:
                raise

        def test_29(self):
            text = """
                \n\n// /*<<[ ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.NamelessBlockError as e:
                assert str(e) == "Nameless block '<<[ ]>>' at line 4, column 6"
            except Exception:
                raise

        def test_30(self):
            text = """
                \n\n// /*<<[ block1 ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 4, column 6"
            except Exception:
                raise

        def test_31(self):
            # Block inside another block is considered part of the outer block
            text = """
                \n\n// /*<<[ block1 ]>>*/
                           /*<<[ block2 ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 4, column 6"
            except Exception:
                raise

        def test_32(self):
            # Empty block name inside another block is not considered an error
            text = """
                \n\n// /*<<[ block1 ]>>*/
                           /*<<[ ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 4, column 6"
            except Exception:
                raise

        def test_33(self):
            text = """
                \n\n// /*<<[ block1 ]>>*/
                           /*<<[ block2 ]>>*/
                               /*<<[ ]>>*//*<<[ end ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 4, column 6"
            except Exception:
                raise

        def test_34(self):
            text = """
                \n\n// /*<<[ block1 ]>>*/
                           /*<<[ block2 ]>>*/
                               /*<<[ end ]>>*//*<<[ ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingBlockEndMarkerError as e:
                assert str(e) == "Missing block end marker '<<[ end ]>>' for block '<<[ block1 ]>>' at line 4, column 6"
            except Exception:
                raise

        def test_35(self):
            text = """
                \n\n// /*<<[ block1 ]>>*//*<<[ end ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '/*<<[ block1 ]>>*//*<<[ end ]>>*/' at line 4, column 6" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_36(self):
            text = """
                \n\n// /*<<[ block1 ]>>*//*<<[block2]>>*//*<<[end]>>*//*<<[ end ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '/*<<[ block1 ]>>*//*<<[block2]>>*//*<<[end]>>*//*<<[ end ]>>*/' at line 4, column 6" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_37(self):
            text = """
                // <<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.UnmatchedBlockEndMarkerError as e:
                assert str(e) == "Unmatched block end marker '<<[ end ]>>' at line 2, column 20"
            except Exception:
                raise

        def test_38(self):
            text = """
                \n\n<<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.UnmatchedBlockEndMarkerError as e:
                assert str(e) == "Unmatched block end marker '<<[ end ]>>' at line 4, column 1"
            except Exception:
                raise

        def test_39(self):
            text = """
                <<[ block1 ]>>
                <<[ end ]>>
                <<[ block1 ]>>
                <<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.DuplicatedBlockExpressionError as e:
                assert str(e) == "Duplicated block '<<[ block1 ]>>' with same expression 'block1' at line 4, column 17"
            except Exception:
                raise

        def test_40(self):
            text = """
                /*<<[ block1 ]>>*//*<<[ end ]>>*/
                /*<<[ block2 ]>>*//*<<[ end ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '/*<<[ block1 ]>>*//*<<[ end ]>>*/' at line 2, column 19" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_41(self):
            text = """
                /*<<[ block1 ]>>*/ /*<<[ end ]>>*/
                /*<<[ block2 ]>>*//*<<[ end ]>>*/
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.MissingSpacesBetweenBlockMarkersError as e:
                assert str(e) == "Missing spaces between block markers '/*<<[ block2 ]>>*//*<<[ end ]>>*/' at line 3, column 19" \
                                 " (spaces are mandatory to make '/*<<[ block ]>>*/ ... /*<<[ end ]>>*/' style markers work)"
            except Exception:
                raise

        def test_42(self):
            text = """
                <<[ 1block ]>>
                <<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ 1block ]>>' at line 2, column 17:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                if sys.version_info >= (3, 10):
                    assert str(e.__cause__) == "invalid decimal literal (<unknown>, line 1)"
                else:
                    assert str(e.__cause__) == "unexpected EOF while parsing (<unknown>, line 1)"
            except Exception:
                raise

        def test_43(self):
            text = """
                <<[ block1 block2 ]>>
                <<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ block1 block2 ]>>' at line 2, column 17:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                if sys.version_info >= (3, 10):
                    assert str(e.__cause__) == "invalid syntax (<unknown>, line 1)"
                else:
                    assert str(e.__cause__) == "unexpected EOF while parsing (<unknown>, line 1)"
            except Exception:
                raise

        def test_44(self):
            text = """
                <<[ block1('a', '1')) ]>>
                <<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ block1('a', '1')) ]>>' at line 2, column 17:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                assert str(e.__cause__) == "unmatched ')' (<unknown>, line 1)"
            except Exception:
                raise

        def test_45(self):
            text = """
                <<[ block1(end_idx) ]>>
                <<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ block1(end_idx) ]>>' at line 2, column 17:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                if sys.version_info >= (3, 14):
                    assert str(e.__cause__) == "malformed node or string on line 1: Name(id='end_idx', ctx=Load())"
                elif sys.version_info >= (3, 10):
                    assert str(e.__cause__).startswith("malformed node or string on line 1: <ast.Name object at")
                else:
                    assert str(e.__cause__).startswith("malformed node or string: <ast.Name object at")
            except Exception:
                raise

        def test_46(self):
            text = """
                <<[ 123 ]>>
                <<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ 123 ]>>' at line 2, column 17:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                assert str(e.__cause__) == "unexpected type '<class 'ast.Constant'>' for expression: 123"
            except Exception:
                raise

        def test_47(self):
            text = """
                <<[ block(a=1, a=1) ]>>
                <<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ block(a=1, a=1) ]>>' at line 2, column 17:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                assert str(e.__cause__) == "keyword argument repeated: a"
            except Exception:
                raise

        def test_48(self):
            text = """
                <<[ block(a=1, 2) ]>>
                <<[ end ]>>
            """
            try:
                blockgen.string.remove_markers(text)
                assert False
            except blockgen.BlockExpressionError as e:
                assert str(e) == "Invalid block expression '<<[ block(a=1, 2) ]>>' at line 2, column 17:\n" \
                                 "    1) look at the inner exception for more details\n" \
                                 "    2) block names can only contain alphanumeric characters (a-zA-Z0-9) or underscores (_), and cannot start with a number\n" \
                                 "    3) parameters must be a valid Python expression containing only literals (ex: 'block('a', 1, param=[1, 2, 3])')"
                assert str(e.__cause__) == "positional argument follows keyword argument (<unknown>, line 1)"
            except Exception:
                raise

    class Test_Multiline_Options:

        def test_1(self):
            try:
                os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"] = "((("
                text = """((( block1 ]>>\nabc\n((( end ]>>"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == "abc\n"
            finally:
                del os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"]

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == "abc\n"

        def test_2(self):
            try:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL("(((")
                text = """((( block1 ]>>\nabc\n((( end ]>>"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == "abc\n"
            finally:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL(None)

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == "abc\n"

        def test_3(self):
            blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL("<<[")
            with blockgen.options(open_marker_literal="((("):
                text = """((( block1 ]>>\nabc\n((( end ]>>"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == "abc\n"

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == "abc\n"

        def test_4(self):
            try:
                os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"] = ")))"
                text = """<<[ block1 )))\nabc\n<<[ end )))"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == "abc\n"
            finally:
                del os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"]

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == "abc\n"

        def test_5(self):
            try:
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(")))")
                text = """<<[ block1 )))\nabc\n<<[ end )))"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == "abc\n"
            finally:
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(None)

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == "abc\n"

        def test_6(self):
            blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL("]>>")
            with blockgen.options(close_marker_literal=")))"):
                text = """<<[ block1 )))\nabc\n<<[ end )))"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == "abc\n"

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == "abc\n"

        def test_7(self):
            try:
                os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"] = "@@@"
                text = """<<[ block1 ]>>\nabc\n<<[ @@@ ]>>"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == "abc\n"
            finally:
                del os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"]

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == "abc\n"

        def test_8(self):
            try:
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION("@@@")
                text = """<<[ block1 ]>>\nabc\n<<[ @@@ ]>>"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == "abc\n"
            finally:
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION(None)

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == "abc\n"

        def test_9(self):
            blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION("end")
            with blockgen.options(end_block_expression="@@@"):
                text = """<<[ block1 ]>>\nabc\n<<[ @@@ ]>>"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == "abc\n"

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == "abc\n"

        def test_10(self):
            try:
                os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"] = "((("
                os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"] = ")))"
                os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"] = "@@@"
                text = """((( block1 )))\nabc\n((( @@@ )))"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == "abc\n"
            finally:
                del os.environ["BLOCKGEN_OPEN_MARKER_LITERAL"]
                del os.environ["BLOCKGEN_CLOSE_MARKER_LITERAL"]
                del os.environ["BLOCKGEN_END_BLOCK_EXPRESSION"]

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == "abc\n"

        def test_11(self):
            try:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL("(((")
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(")))")
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION("@@@")
                text = """((( block1 )))\nabc\n((( @@@ )))"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == "abc\n"
            finally:
                blockgen.set_env_BLOCKGEN_OPEN_MARKER_LITERAL(None)
                blockgen.set_env_BLOCKGEN_CLOSE_MARKER_LITERAL(None)
                blockgen.set_env_BLOCKGEN_END_BLOCK_EXPRESSION(None)

            text = """<<[ block1 ]>>\nabc\n<<[ end ]>>"""
            new_text = blockgen.string.remove_markers(text)
            assert new_text == "abc\n"

        def test_12(self):
            with blockgen.options(open_marker_literal="[[[",
                                  close_marker_literal="]]]",
                                  end_block_expression="&&&"):
                with blockgen.options(open_marker_literal="(((",
                                      close_marker_literal=")))",
                                      end_block_expression="@@@"):
                    text = """((( block1 )))\nabc\n((( @@@ )))"""
                    new_text = blockgen.string.remove_markers(text)
                    assert new_text == "abc\n"

                text = """[[[ block1 ]]]\nabc\n[[[ &&& ]]]"""
                new_text = blockgen.string.remove_markers(text)
                assert new_text == "abc\n"
