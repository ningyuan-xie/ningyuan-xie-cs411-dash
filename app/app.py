# app.py - Main entry point for the Dash app.

import os
from dash import Dash
from app.layout import *
from app.callbacks import *
from app.neo4j_utils import start_neo4j_keep_alive
from app.mysql_utils import start_mysql_keep_alive
from app.memory_utils import start_memory_cleanup


def create_app() -> Dash:
    """Create and initialize the Dash app."""
    app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
    app.title = "Exploring Academic World"
    app.layout = create_layout()
    return app


# Global app instance for Gunicorn
app = create_app()

# Start background processes
start_neo4j_keep_alive()
start_mysql_keep_alive()
start_memory_cleanup(interval_seconds=30)


if __name__ == "__main__":
    # True locally, False on Render
    is_local = os.environ.get("RENDER") is None

    app.run(
        debug=is_local,
        use_reloader=is_local,
        dev_tools_hot_reload=False,
        host="0.0.0.0",
        port="8050"
    )
