import typing
from pentagraph.lib.graph import Board


def render(board: Board, fullscreen: bool = True, base: int = 300) -> None:
    """Starts local flask server with render template"""
    from flask import Flask, render_template
    from ujson import dump
    from os import path

    app = Flask(__name__, template_folder="template", static_folder="static")

    with open(f"{path.dirname(path.realpath(__file__))}/static/dump.json", "w+") as F:
        dump(board.jsonify(), F)

    @app.route("/")
    def render_route():
        return render_template("penta.html")

    return app.run(debug=True)
