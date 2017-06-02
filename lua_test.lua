-- Rust C-ABI library template - Python test harness
--
-- Copyright (c) 2017 Sean Bolton
--
-- Permission is hereby granted, free of charge, to any person obtaining
-- a copy of this software and associated documentation files (the
-- "Software"), to deal in the Software without restriction, including
-- without limitation the rights to use, copy, modify, merge, publish,
-- distribute, sublicense, and/or sell copies of the Software, and to
-- permit persons to whom the Software is furnished to do so, subject to
-- the following conditions:
--
-- The above copyright notice and this permission notice shall be
-- included in all copies or substantial portions of the Software.
--
-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
-- EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
-- MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
-- NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
-- LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
-- OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
-- WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

local ffi = require("ffi")

ffi.cdef[[
    typedef struct _CallResult {
        int32_t status;
        char *  text;
    } CallResult;

    CallResult *rust_function(const char *);
    void        free_result(CallResult *);
]]

local rustlib = ffi.load("target/debug/librust_c_abi_library_template.so")

assert(rustlib)
assert(ffi.C.rust_function)
assert(ffi.C.free_result)

local result = ffi.C.rust_function("success")
local status = result.status
local text = ffi.string(result.text)
ffi.C.free_result(result)
print(string.format("call with 'success' returned (%d, '%s')", status, text))
assert(status == 0)
assert(text == "Success!")

result = ffi.C.rust_function("failure")
status = result.status
text = ffi.string(result.text)
ffi.C.free_result(result)
print(string.format("call with 'failed' returned (%d, '%s')", status, text))
assert(status == 1)
assert(text == "Failure :(")

result = ffi.C.rust_function("panic")
status = result.status
text = ffi.string(result.text)
ffi.C.free_result(result)
print(string.format("call with 'panic' returned (%d, '%s')", status, text))
assert(status == 2)
assert(text == "I have no towel")
