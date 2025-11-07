# app.py - Main entry point for the Dash app.

import os
from dash import Dash
from layout import create_layout
from callbacks import *
from neo4j_utils import start_neo4j_keep_alive
from mysql_utils import start_mysql_keep_alive
from memory_utils import start_memory_cleanup


def create_app() -> Dash:
    app = Dash(
        __name__,
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )
    app.title = "Exploring Academic World"
    app.layout = create_layout()
    return app


# Create global Dash instance for Gunicorn
app = create_app()

# Start background keep-alive and memory cleanup threads
start_neo4j_keep_alive()
start_mysql_keep_alive()
start_memory_cleanup(interval_seconds=300)


if __name__ == "__main__":
    # True locally, False on Render
    is_local = os.environ.get("RENDER") is None

    app.run(
        debug=is_local,
        use_reloader=is_local,
        host="0.0.0.0",
        port=8050
    )
