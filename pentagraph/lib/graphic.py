import typing
from .graph import RawBoard


def render(rawboard: RawBoard, fullscreen: bool = True, base: int = 300) -> None:
    """Starts local flask server with render template"""
    from flask import Flask, render_template, request, jsonify, abort
    from os import path

    app = Flask(__name__, template_folder="template", static_folder="static")

    @app.route("/")
    def render_route():
        return render_template("penta.html")

    @app.route("/data")
    def data_board():
        return jsonify(rawboard.jsonify(hexcolors=True))

    @app.route("/reset")
    def reset_board():
        board = RawBoard(generate=True)
        return render_route()

    @app.route("/update")
    def update_graph():
        if "move" not in request.values:
            return abort(401)
        rawboard.move(request.values())
        return jsonify(rawboard.jsonify())

    @app.route("/add-figures")
    def add_figures_route():
        figures = request.values.get("figures", None)
        if figures is None:
            return abort(401)
        rawboard.add_figures(figures)
        return jsonify(rawboard.jsonify(hexcolors=True))

    return app.run(debug=True)
