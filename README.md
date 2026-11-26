# tep-python-packages

A static Python package index (PEP 503) on GitHub Pages:

    https://the-everyone-project.github.io/tep-python-packages/simple/

It serves the wheels of our Tumult forks
([tumult-core](https://github.com/The-Everyone-Project/tumult-core),
[tumult-analytics](https://github.com/The-Everyone-Project/tumult-analytics))
to difference-engine.

## Why not the release URLs

A GitHub Release download redirects to a signed storage URL. Dependabot's
proxy sends its GitHub token along with that redirect, the storage service
rejects the request with a 401, and every Dependabot update in
difference-engine failed. Pages serves the files directly, so there is no
redirect (TEP2-390).

## How it updates

`.github/workflows/publish-index.yml` runs daily, on push and by hand. It
downloads every wheel from the published (not draft, not pre-release)
releases of each repo in `sources.txt`, and rebuilds the whole site with
`scripts/build_index.py`. The forks are only read, never changed.

To publish a new fork build: cut the release on the fork, then run the
workflow by hand (or wait a day). difference-engine pins the exact build in
`constraint-dependencies`, so adding a build here never changes what it uses.

Do not delete a fork release that a difference-engine lock still uses: the
wheel would drop out of the index and `uv sync` would fail.
