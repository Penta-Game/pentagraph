# pentagraph

Graph representation and tools for programming with the pentagame board

## Setup

To install the basic dependencies you can use `pip`: `python3 -m pip install -r requirements.txt`

I highly recommend using a [virtualenv](https://docs.python.org/3/library/venv.html) for developing purposes.

## License

The source code of pentagraph is distributed according to the [MIT License by Cobalt](https://github.com/Penta-Game/pentagraph/blob/master/LICENSE)

Libraries as listed in `requirements.txt` please consider their respective Licenses before e.g. making commercial use of `pentagraph`.

## Development Notes

### pentagraph.lib.graphic

An easy-to-use way of displaying the `Board` taking advantage of Flask in combination with [materialize css](https://materializecss.com/), [svg.js](https://svgjs.com/docs/3.0) and [jquery](). The final board svg is created with a variation of resources from [boardgame](https://github.com/Penta-Game/boardgame).

### pentagraph.lib.figures

Collection of Objects used for figure representation. These Objects also specifiy their respective drawing methods and types.

### pentagraph.lib.graph

Graph representation as `Board` Object.

### pentagraph.lib.constants

Constants used for board graphics. May be used to construct a pentagame board in 2D space.

### pentagraph.ml

Reserved space for machine learning with pentagame graphs. Will in the future require tensorflow, gym and other libraries.
