#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Rust C-ABI library template - Python test harness
#
# Copyright (c) 2017 Sean Bolton
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import unicode_literals

import unittest

class TestRustLibrary(unittest.TestCase):

    def test_library(self):
        import ctypes
        from ctypes import (POINTER, c_char_p, c_int32)

        class CallResult(ctypes.Structure):
            _fields_ = [("status", c_int32), ("text", c_char_p)]

        lib = ctypes.cdll.LoadLibrary("target/debug/librust_c_abi_library_template.so")

        call_rust = lib.rust_function
        call_rust.argtypes = (c_char_p, )
        call_rust.restype = POINTER(CallResult)

        free_result = lib.free_result
        free_result.argtypes = (POINTER(CallResult), )
        free_result.restype = None

        def get_result(s):
            ptr = call_rust(s)
            try:
                return (ptr[0].status, ptr[0].text.decode('utf-8'))
            finally:
                free_result(ptr)

        self.assertEqual(get_result('success'.encode('utf-8')), (0, 'Success!'))
        self.assertEqual(get_result('failure'.encode('utf-8')), (1, 'Failure :('))
        self.assertEqual(get_result('panic'.encode('utf-8')), (2, 'I have no towel'))
        # force a panic in the wrapped code by passing bad UTF-8
        self.assertEqual(get_result('aña'.encode('latin-1')),
                         (2, "called `Result::unwrap()` on an `Err` value: Utf8Error { valid_up_to: 1 }"))

if __name__ == '__main__':
    unittest.main()
