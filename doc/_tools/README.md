# Extraction tools

These scripts generated the reference pages in this directory tree. They need Python 3 with
`capstone`, `pyelftools` and `protobuf`. On NixOS:

```sh
nix shell --impure --expr 'with import (builtins.getFlake "nixpkgs") {}; python3.withPackages (p: [p.capstone p.pyelftools p.protobuf])'
```

## Pipeline

1. **Fetch the client.** Download `https://client-update.steamstatic.com/steam_client_ubuntu12` (a VDF
   manifest), then download each `"file"` it lists from the same host and unzip them all into one root.
   Some archives use Windows `\` path separators; normalise those to `/`.
2. **`callargs.py <elf>` → JSONL.** Linear-sweeps `.text` with capstone, in 64 KiB windows so memory stays
   bounded, and tracks register contents (including callee-saved registers and reg→reg moves). It writes one
   line per `call`, giving the target (resolved through PLT/GOT and `.symtab` where possible) and every
   argument register that holds a recoverable constant: a C string via `lea [rip+X]` or an absolute
   immediate, an integer, or a float.
3. **`rank.py <jsonl>`** (exploratory). Ranks call targets by how registration-shaped their arguments look,
   for example `(this, "name", "default", flags, "help")`. Use it to find internal ConVar constructors and
   argv/env helpers in a new build.
4. **`aggregate.py`** classifies all call sites into records (`records.json`): known imports (`getenv`,
   `SteamStdLib::CCommandLineParam`, `Plat_CommandLineParam*`, `SDL_SetHint`, ...), shape-detected
   ConVar/ConCommand constructors and argv parsers, plus a small hand-verified `WHITELIST` of internal
   accessors. The whitelisted addresses are build-specific and must be re-checked with `rank.py` for a new build.
5. **`render.py`** writes `binaries/*.md`.
6. **`protodump.py <outdir> <elf>...`** carves serialized `FileDescriptorProto`s out of the binaries and prints
   them as `.proto` text (`../protobuf/`). **`settings2md.py steamui.so <out.md>`** renders
   `CMsgClientSettings` together with its custom field options (`../settings/client-settings.md`).
7. **`usage.py <elf> <binary-key> records.json <calls.jsonl>`** collects usage context for each record:
   strings near the call site, or near every access to a ConVar object. Function boundaries come from
   `.eh_frame_hdr`. **`mkctx.py`** turns that into per-category context files. Those files were used to write the
   "What it does" descriptions ([descriptions/](descriptions/)*.json; copy them to `desc/` before running
   `render.py` and `settings2md.py`).

## Limitations

* Only the x86-64 binaries are analysed. The 32-bit `ubuntu12_32/` builds are the same code base. The
  analysis is static, so it misses names built at runtime (string concatenation, tables read from data
  files).
* Arguments loaded through memory indirection (other than RELATIVE-relocated pointer slots) are not recovered.
  These show up as missing defaults or help text.
