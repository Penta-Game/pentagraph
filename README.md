[![Python Version](https://img.shields.io/badge/python-3.8.2-blue?style=for-the-badge&logo=python)](https://www.python.org/downloads/release/python-382/) [![Code Style](https://img.shields.io/badge/Style-black-%23000000?style=for-the-badge)](https://black.readthedocs.io/) [![Networkx Version](https://img.shields.io/badge/NetworkX-2.4-orange?style=for-the-badge)](https://networkx.github.io/) [![Version](https://img.shields.io/badge/Version-Beta-red?style=for-the-badge)](https://pypi.org/project/pentagraph/)

# pentagraph

Graph representation and tools for programming with pentagame. *This is in active development an will be fully functional with the 0.0.1 release*

## Setup

### Pip

You will need a working instance of [pip](https://www.makeuseof.com/tag/install-pip-for-python/).

`python3 -m pip install pentagraph`

### Development

Clone from github (requires [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)): `git clone https://github.com/Penta-Game/pentagraph`

To install the basic dependencies you can use `pip`: `python3 -m pip install -r requirements.txt`

I highly recommend using a [virtualenv](https://docs.python.org/3/library/venv.html) for developing purposes.

## License

The source code of pentagraph is distributed according to the [MIT License by Cobalt](https://github.com/Penta-Game/pentagraph/blob/master/LICENSE)

Libraries as listed in `requirements.txt` please consider their respective Licenses before e.g. making commercial use of `pentagraph`.

## Development Notes

### `pentagraph.lib.graphic`

An easy-to-use way of displaying the `Board` taking advantage of Flask in combination with [materialize css](https://materializecss.com/), [svg.js](https://svgjs.com/docs/3.0). The final board svg is created with a variation of resources from [boardgame](https://github.com/Penta-Game/boardgame).

### `pentagraph.lib.figures`

Collection of Objects used for figure representation. These Objects also specifiy their respective drawing methods and types.

### `pentagraph.lib.graph`

Graph representation as `Board` Object.

### `pentagraph.lib.constants`

Constants used for board graphics. May be used to construct a pentagame board in 2D space.

### `pentagraph.ml`

Reserved space for machine learning with pentagame graphs. Will in the future require tensorflow, gym and other libraries.
