/* Rust C-ABI library template - Python test harness
 *
 * Copyright (c) 2017 Sean Bolton
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

/* compile and run this with something like:
 * $ cargo build
 * $ gcc -Wall -O2 -o c_test c_test.c -L target/debug -lrust_c_abi_library_template
 * $ LD_LIBRARY_PATH=target/debug ./ffi_test
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef struct _CallResult {
    int32_t status;
    char *  text;
} CallResult;

extern CallResult *rust_function(const char *);
extern void        free_result(CallResult *);

int
main(void) {
    CallResult *cr = rust_function("success");

    assert(cr != NULL);
    assert(cr->text != NULL);
    printf("call with 'success' returned (%d, '%s')\n", cr->status, cr->text);
    assert(cr->status == 0);
    assert(!strcmp(cr->text, "Success!"));
    free_result(cr);

    cr = rust_function("failure");
    assert(cr != NULL);
    assert(cr->text != NULL);
    printf("call with 'failure' returned (%d, '%s')\n", cr->status, cr->text);
    assert(cr->status == 1);
    assert(!strcmp(cr->text, "Failure :("));
    free_result(cr);

    cr = rust_function("panic");
    assert(cr != NULL);
    assert(cr->text != NULL);
    printf("call with 'panic' returned (%d, '%s')\n", cr->status, cr->text);
    assert(cr->status == 2);
    assert(!strcmp(cr->text, "I have no towel"));
    free_result(cr);

    return 0;
}
