import unittest

class TestRustModule(unittest.TestCase):

    def test_module(self):
        import ctypes
        from ctypes import (POINTER, c_char_p, c_int32)

        class CallResult(ctypes.Structure):
            _fields_ = [("status", c_int32), ("text", c_char_p)]

        peglib = ctypes.cdll.LoadLibrary("target/debug/libabcparser_peg.so")

        canonify_music_code = peglib.canonify_music_code
        canonify_music_code.argtypes = (c_char_p, )
        canonify_music_code.restype = POINTER(CallResult)

        free_result = peglib.free_result
        free_result.argtypes = (POINTER(CallResult), )
        free_result.restype = None

        def get_result(s):
            ptr = canonify_music_code(s)
            try:
                return (ptr[0].status, ptr[0].text.decode('utf-8'))
            finally:
                free_result(ptr)

        self.assertEqual(get_result('abc|def'.encode('utf-8')), (0, 'abc|def'))
        (status, message) = get_result('aXXo982027bc|def'.encode('utf-8'))
        expected = "ABC parse failed at character 4, matched 'aXXo', could not match '982027bc|d...', expected ["
        self.assertEqual(status, 1)
        self.assertTrue(message.startswith(expected),
                        msg="looking for '{}', found '{}'".format(expected, message))
        self.assertEqual(get_result('aña'.encode('latin-1')),
                         (2, "called `Result::unwrap()` on an `Err` value: Utf8Error { valid_up_to: 1 }"))

if __name__ == '__main__':
    unittest.main()
