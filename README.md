# URI Gatherer
Python script to recursively gather unique URIs from the links found within a seed URI.

## Requirements
* [Python 3.10+](https://www.python.org/)

Dependencies are managed with [uv](https://docs.astral.sh/uv/):
```
uv sync
```

## Usage

```
uri-gatherer [-h] [-T [timeout]] [-v] [-d] seed_uri [unique_count]
```

Run with `uv`:
```
uv run uri-gatherer https://weiglemc.github.io/ 50
```

Results are written to a `{date}-uris.txt` file in the current directory and printed to the console.

## Sample Output

```
https://www.odu.edu/facultydevelopment/women-in-stem#tab9=3&done1612907281342
https://arxiv.org/abs/2308.05038
https://twitter.com/weiglemc
https://arxiv.org/abs/2401.04887
https://weiglemc.github.io/contact/
https://www.odu.edu/computer-science/academics/graduate/phd
```

## Development

Install all dependency groups:
```
uv sync --all-groups
```

| Command | Description |
|---|---|
| `uv run poe test` | Run unit tests with coverage |
| `uv run poe fulltest` | Run all tests including live network integration tests |
| `uv run poe format` | Format and sort imports with ruff |
| `uv run poe lint` | Run mypy, ruff, and pylint |
