# Contributing to PassTUI

PassTUI is open to contributions!

## Development

First, you will need to install [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage the development dependencies.

Then, setup an environment for development, run:

```bash
uv sync
```

Once the sync process is finished, you should have a virtual environment with the dependencies installed.

Activate the virtual environment:

```bash
source .venv/bin/activate
```

To start in development mode, run:

```bash
textual console
```

Then in another terminal, run:

```bash
TEXTUAL=devtools,debug passtui
```

### Running the tests

Be sure to use the `Makefile` commands.

```bash
make test
```
