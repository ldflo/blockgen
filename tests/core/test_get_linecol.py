import blockgen

class Test:

    def test_1(self):
        assert blockgen.core._get_linecol("abc\ndef\nghi", 0) == (1, 1)
        assert blockgen.core._get_linecol("abc\ndef\nghi", 1) == (1, 2)
        assert blockgen.core._get_linecol("abc\ndef\nghi", 2) == (1, 3)
        assert blockgen.core._get_linecol("abc\ndef\nghi", 3) == (1, 4)
        assert blockgen.core._get_linecol("abc\ndef\nghi", 4) == (2, 1)
        assert blockgen.core._get_linecol("abc\ndef\nghi", 5) == (2, 2)
        assert blockgen.core._get_linecol("abc\ndef\nghi", 6) == (2, 3)
        assert blockgen.core._get_linecol("abc\ndef\nghi", 7) == (2, 4)
        assert blockgen.core._get_linecol("abc\ndef\nghi", 8) == (3, 1)
        assert blockgen.core._get_linecol("abc\ndef\nghi", 9) == (3, 2)
        assert blockgen.core._get_linecol("abc\ndef\nghi", 10) == (3, 3)
        assert blockgen.core._get_linecol("abc\ndef\nghi", 11) == (3, 4)
