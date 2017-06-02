// Rust C-ABI library template
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

// Note: currently, catch_unwind() has to spin up a new thread to be able to
// catch panics. See Balasubramanian et al., "System Programming in Rust:
// Beyond Safety", https://www.sigops.org/hotos/hotos17/papers/hotos17-final92.pdf
// for thoughts on other ways to do this.

use std::panic::catch_unwind;
use std::ffi::{CStr,CString};
use std::os::raw::c_char;

#[derive(Debug)]
#[repr(C)]
pub struct CallResult {
   status: i32,       // 0: success,      1: failure,         2: panic caught
   text: *mut c_char  // success message, failure message, or panic message
}

#[no_mangle]
pub extern "C" fn rust_function(raw_input: *const c_char) -> *mut CallResult {
    let catch_result: Result<CallResult, _> = catch_unwind(|| {
        assert!(!raw_input.is_null());
        let c_str = unsafe { CStr::from_ptr(raw_input) };
        // here we assume the caller will pass valid UTF-8, otherwise we panic
        let input = c_str.to_str().unwrap();
        //println!("Rust library: got '{}'", input);

        match input {
            "success" => CallResult { status: 0,
                                      text: CString::new("Success!").unwrap().into_raw() },
            "failure" => {
                let s: String = format!("Failure {}", ":(");
                // CString::new(s).unwrap() will panic if s contains any 0 bytes
                CallResult { status: 1, text: CString::new(s).unwrap().into_raw() }
            },
            "panic" => {
                //let n: Option<i32> = None;
                //n.unwrap();  // force a panic
                //unreachable!()
                panic!("I have no towel");
            },
            _ => CallResult { status: 1,
                              text: CString::new("unrecognized input").unwrap().into_raw() },
        }
    });
    let final_result: CallResult;
    match catch_result {
        Ok(result) => { final_result = result; }
        Err(error) => {  // the closure panicked, so try to get an error message
            let return_str: &str;
            // why does catch_unwind() throw away the location information?
            //   -> libstd/panicking.rs:try()
            //   -> src/libpanic_unwind/lib.rs:__rust_maybe_catch_panic() discards the location
            //      (file and line) information (if it was ever valid), so the cause is the most
            //      we can retreive:
            if let Some(rs) = error.downcast_ref::<&'static str>() {
                return_str = *rs;
            } else if let Some(rs) = error.downcast_ref::<String>() {
                return_str = &rs[..];
            } else {
                return_str = "Panic!";
            }
            final_result = CallResult {
                               status: 2, text: CString::new(return_str).unwrap().into_raw()
                           };
        }
    }
    //let p = Box::into_raw(Box::new(final_result));
    //println!("{:?}", p);
    //p
    Box::into_raw(Box::new(final_result))
}

#[no_mangle]
pub extern "C" fn free_result(p: *mut CallResult) {
    if !p.is_null() {
        //println!("{:?}", p);
        unsafe {
            let b = Box::from_raw(p);
            CString::from_raw(b.text);
        }
    }
}
