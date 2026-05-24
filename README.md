# URI Gatherer
Python3 script to gather unique URIs from the links found within a seed URI.

## Requirements
* [Python 3.10](https://www.python.org/)

Dependencies are managed with [uv](https://docs.astral.sh/uv/):
`uv sync`

## Running Instructions
This program can be executed using `./gather-uris.py [URI]` where the URI is valid
and contains link tags. The number of links this program will search for can be
edited by supplying an integer value after the URI: `./gather-uris.py [URI] [number]`.
All further command line arguments and flags can be found using
`./gather-uris.py --help`.

## Sample Execution
When this program is run with the following arguments:
`./gather-uris.py https://weiglemc.github.io/`

A new file named `{date}-uris.txt` is created and the console output
will be similar to:
```
https://www.odu.edu/facultydevelopment/women-in-stem#tab9=3&done1612907281342
https://arxiv.org/abs/2308.05038
https://twitter.com/weiglemc
https://arxiv.org/abs/2401.04887
https://weiglemc.github.io/contact/
https://www.odu.edu/computer-science/academics/graduate/phd
```
