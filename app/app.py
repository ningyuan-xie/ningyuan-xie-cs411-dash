# app.py - Main entry point for the Dash app.

import os
from dash import Dash
from layout import *
from callbacks import *
from neo4j_utils import start_neo4j_keep_alive
from mysql_utils import start_mysql_keep_alive
from memory_utils import start_memory_cleanup


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
    
    # Start Neo4j keep-alive background process
    start_neo4j_keep_alive()
    
    # Start MySQL keep-alive background process
    start_mysql_keep_alive()
    
    # Start background memory cleanup (runs gc.collect() periodically)
    start_memory_cleanup(interval_seconds=180)
    
    # Check if running in production (Render sets RENDER environment variable)
    is_production = os.getenv("RENDER") == "true" or os.getenv("ENV") == "production"
    debug_mode = os.getenv("DEBUG", "false").lower() == "true" and not is_production
    
    app.run(
        debug=debug_mode,
        use_reloader=debug_mode,  # Only enable reloader in debug mode
        dev_tools_hot_reload=False,
        host='0.0.0.0',
        port=int(os.getenv("PORT", "8050"))
    )
