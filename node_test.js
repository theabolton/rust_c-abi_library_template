// Rust C-ABI library template - Node.js test harness
//
// Copyright (c) 2017 Sean Bolton
//
// Permission is hereby granted, free of charge, to any person obtaining
// a copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to
// permit persons to whom the Software is furnished to do so, subject to
// the following conditions:
//
// The above copyright notice and this permission notice shall be
// included in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
// NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
// LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
// OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
// WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

const assert = require('assert');
const ffi = require('ffi');  // https://github.com/node-ffi/node-ffi/wiki/Node-FFI-Tutorial
const ref = require('ref');  // https://tootallnate.github.io/ref/
const StructType = require('ref-struct');  // https://github.com/TooTallNate/ref-struct

const CallResult = StructType({
  'status': 'int32',
  'text':   'string'
});

const CallResultPtr = ref.refType(CallResult);

const rustlib = ffi.Library('target/debug/librust_c_abi_library_template', {
    rust_function: [CallResultPtr, ['string']],
    free_result: ['void', [CallResultPtr]],
});

function get_result(request) {
    const result = rustlib.rust_function(request);
    try {
        return { status: result.deref().status, text: result.deref().text };
    } finally {
        rustlib.free_result(result);
    }
}

result = get_result('success');
console.log("call with 'success' returned (" + result.status + ", '" + result.text + "')");
assert.equal(result.status, 0);
assert.equal(result.text, 'Success!');

result = get_result('failure');
console.log("call with 'failure' returned (" + result.status + ", '" + result.text + "')");
assert.equal(result.status, 1);
assert.equal(result.text, 'Failure :(');

result = get_result('panic');
console.log("call with 'panic' returned (" + result.status + ", '" + result.text + "')");
assert.equal(result.status, 2);
assert.equal(result.text, 'I have no towel');

