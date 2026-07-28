# Claim 4 method

The fixed cumulative command downloads the primary 624 MB Scale-2 archive
with an explicit User-Agent, verifies its byte count and SHA-256, and extracts
it with a separately pinned official 7-Zip 25.01 binary. It compares the 7-Zip
member listing with the extracted filenames, hashes every GraphML, parses
every `dn_multiscaleID`, and groups all sessions by lexical subject ID.

An independent checker reconstructs subject IDs from filenames and directly
reparses the counterexample GraphML with a separate XML code path. The
negative control proposes padding IDs 169 and 170; it must be rejected because
those nodes do not exist in the archive.

Estimated active cores are four during extraction and one during the
exhaustive parse. Hugging Face `cpu-upgrade` is mandatory because download,
extraction, and parse runtime are uncertain.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```
