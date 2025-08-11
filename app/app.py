# app.py - Main entry point for the Dash app.

from dash import Dash
from layout import *
from callbacks import *
from neo4j_utils import start_neo4j_keep_alive
from mysql_utils import start_mysql_keep_alive


def create_app() -> Dash:
    """Create and initialize the Dash app."""
    # Initialize Dash App
    app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
    app.title = "Exploring Academic World"

    # Set app layout
    app.layout = create_layout()

    return app


# Run the app
if __name__ == '__main__':
    app = create_app()
    
    # Start MySQL keep-alive background process
    start_mysql_keep_alive()

    # Start Neo4j keep-alive background process
    start_neo4j_keep_alive()
    
    app.run(
        debug=True,
        use_reloader=True,
        dev_tools_hot_reload=False,
        host='0.0.0.0',
        port="8050"
    )
