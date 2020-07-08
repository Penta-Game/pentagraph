# pentagraph

Graph representation and tools for programming with the pentagame board

## Setup

To install the basic dependencies you can use `pip`: `python3 -m pip install -r requirements.txt`

To take advantage of the `pentagraph.lib.graphic` utils (e.g. rendering of the `Board`) you will need to use `requirements-qt.txt` (`python3 -m pip install -r requirements-qt.txt`) instead. This will include `PyQt5` (Qt5). [Qt5 uses a LGPL 3 License](https://doc.qt.io/qt-5/lgpl.html#lgpl-version-3). [Learn more about \(Py\)Qt Licensing](https://riverbankcomputing.com/commercial/license-faq). You don't need Qt to use graph or ml functionality.

I highly recommend using a [virtualenv](https://docs.python.org/3/library/venv.html) for developing purposes.

## License

The source code of pentagraph is distributed according to the [MIT License by Cobalt](https://github.com/Penta-Game/pentagraph/blob/master/LICENSE)

Libraries as listed in `requirements.txt`:

- [Networkx](https://networkx.github.io/documentation/networkx-1.10/reference/legal.html#license)
- [Decorator](https://github.com/micheles/decorator/blob/master/LICENSE.txt)
- [Python 3](https://docs.python.org/3/license.html#terms-and-conditions-for-accessing-or-otherwise-using-python)

Libraries as listen in `requirements-qt.txt`:

- All libraries from `requirements.txt`
- [PyQt5](https://doc.qt.io/qt-5/lgpl.html#lgpl-version-3) and [Qt5](https://doc.qt.io/qt-5/lgpl.html#lgpl-version-3)