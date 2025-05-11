# app.py - Main entry point for the Dash app.

from dash import Dash
from mysql_utils import *
from mongodb_utils import *
from neo4j_utils import *
from layout import *
from callbacks import *
from keep_alive import start_keep_alive


def create_app() -> Dash:
    """Creates and initializes the Dash app."""
    # Initialize Dash App
    app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
    app.title = "Exploring Academic World"

    # Initialize MySQL tables, MongoDB collections, and Neo4j labels
    mysql_tables = get_all_tables()
    mongo_collections = get_all_collections()
    neo4j_labels = get_all_labels()

    # Set app layout
    app.layout = create_layout(mysql_tables, mongo_collections, neo4j_labels)

    return app


# Run the app
if __name__ == '__main__':
    app = create_app()
    start_keep_alive()  # Start the keep-alive scheduler
    app.run(
        debug=True,
        use_reloader=True,
        dev_tools_hot_reload=False,
        host='0.0.0.0',
        port=8050
    )
