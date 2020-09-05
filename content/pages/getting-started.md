Title: Getting started
Date: 2020-3-27 10:20
Modified: 2020-3-27 10:20
Slug: getting-started
lang: en
Authors: Cobalt
Summary: getting started section for pentagraph

You can get the `pentagraph` package from [PyPI](https://pypi.org/project/pentagraph/) with [pip](https://packaging.python.org/key_projects/#pip).

Installation with [pip](https://packaging.python.org/tutorials/installing-packages/#id17):

`pip install pentagraph`

Now you can just import the desired modules in your applications. Here's an example on how to create a complete board graph with all figures in the initial position.

```python
from pentagraph.lib.graph import Board

players = (1, 2, 3,4)  # Player UIDS

G = Board(generate=True)  # Generate refers to the fields/ stops
G.gen_start_field(players)
```
