# Rust C-ABI Library Template

A minimal template for building a Rust library and calling it from C-ABI
langauges including C, JavaScript (Node.js), Lua, and Python.

Also included is a Travis-CI configuration for building a Rust library as part
of a project written in another language (in this case, Python).

## Lua

The lua_test.lua test application was tested using Lua 5.3 with
Pierre Chapuis's fork of [luaffi](https://github.com/catwell/luaffi), which
adds Lua 5.3 to James McKaskill's (unmaintained?) [version](https://github.com/jmckaskill/luaffi).
Either McKaskill's version or the [FaceBook
fork](https://github.com/facebook/luaffifb) will probably work with older
versions of Lua.

Example:

```sh
$ # install luaffi using your favorite method
$ cargo build
$ lua lua_test.lua
```

