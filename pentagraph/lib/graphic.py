import typing
from .graph import Board


def render(board: Board, fullscreen: bool = True, base: int = 300) -> None:
    """Starts local flask server with render template"""
    from flask import Flask, render_template, request, jsonify, abort
    from ujson import dump
    from os import path

    app = Flask(__name__, template_folder="template", static_folder="static")

    with open(f"{path.dirname(path.realpath(__file__))}/static/dump.json", "w+") as F:
        dump(board.jsonify(), F)

    @app.route("/")
    def render_route():
        return render_template("penta.html")

    @app.route("/update")
    def update_graph():
        if "move" not in request.values:
            return abort(401)
        board.move(request.values())
        return jsonify(board.jsonify())

    return app.run(debug=True)
