# callback_graph.py - Utility functions used during callbacks.

from typing import Any, List, Tuple, Union, Sequence
import pandas as pd
from dash import dash_table, html
import plotly.express as px


# Bar chart
def create_bar_chart(data: Sequence[Tuple[str, Union[int, float]]], title: str, 
                     label_x: str, label_y: str, 
                     horizontal: bool = False, database: str = "MongoDB") -> Any:
    """Creates a bar chart using Plotly Express."""
    # Extract x and y based on orientation
    x_vals = [value for _, value in data] if horizontal else [label for label, _ in data]
    y_vals = [label for label, _ in data] if horizontal else [value for _, value in data]

    fig = px.bar(
        x=x_vals,
        y=y_vals,
        text=[str(value) for _, value in data],
        labels={"x": label_x, "y": label_y},
        title=title,
        orientation='h' if horizontal else 'v'
    )

    # Define 4 colors: based on orientation and database
    colors = {
        ("MongoDB", False): "#2ECC71",  # vertical MongoDB - Emerald
        ("MySQL", False): "#1E90FF",    # vertical MySQL - Dodger Blue
        ("MongoDB", True): "#6A5ACD",   # horizontal MongoDB - Slate Blue
        ("MySQL", True): "#FF7F50",     # horizontal MySQL - Coral
    }

    # Pick color
    chosen_color = colors.get((database, horizontal), "#888888")  # fallback gray

    fig.update_traces(
        marker_color=chosen_color,
        textposition='inside',
        textfont_size=14
    )

    if horizontal:
        fig.update_layout(yaxis=dict(autorange='reversed'))

    return fig


# Pie chart
def create_pie_chart(df: pd.DataFrame, names_col: str, 
                     values_col: str, title: str, hole: float = 0.4) -> Any:
    """Creates a pie chart using Plotly Express."""
    fig = px.pie(
        df, 
        names=names_col, 
        values=values_col, 
        title=title,
        hole=hole
    )
    fig.update_traces(textposition='inside', textinfo='label')
    return fig


# Data table
def create_data_table(df: pd.DataFrame) -> Any:
    """Creates a data table using Dash DataTable."""
    return dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        style_table={
            'width': '80%', 'margin': '20px auto', 'borderRadius': '12px',
            'overflowY': 'auto', 'maxHeight': '450px',
            'boxShadow': '2px 2px 10px rgba(0,0,0,0.15)'
        },
        style_cell={
            'textAlign': 'left', 'padding': '16px', 'fontSize': '18px',
            'fontFamily': 'Arial, sans-serif', 'whiteSpace': 'normal', 'height': 'auto'
        },
        style_header={
            'backgroundColor': '#e9eef3', 'fontWeight': 'bold',
            'textAlign': 'center', 'fontSize': '20px', 'padding': '18px'
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#f9fbfc"},
            {"if": {"row_index": "even"}, "backgroundColor": "#ffffff"}
        ]
    )


# Sunburst chart
def create_sunburst_chart(df: pd.DataFrame, path_col: str, 
                          value_col: str, title: str) -> Any:
    """Creates a sunburst chart using Plotly Express."""
    fig = px.sunburst(
        df,
        path=[path_col],
        values=value_col,
        title=title,
        custom_data=[df[value_col]]
    )
    fig.update_layout(
        margin=dict(t=100, l=0, r=0, b=0),
        width=450,
        height=450
    )
    fig.update_traces(textinfo="label+value")
    return fig


# HTML header
def create_section_header(title: str, subtitle: str) -> html.Div:
    """Return a styled section header with a title and a subtitle."""
    return html.Div([
        html.H4(f"{title}", style={"marginBottom": "4px", "fontSize": "20px"}),
        html.H5(subtitle, style={
            "marginTop": "0px",
            "marginBottom": "10px",
            "fontSize": "18px",
            "fontWeight": "normal"
        })
    ])


# HTML table
def create_info_table(headers: List[str], rows: Sequence[Tuple[Any, ...]]) -> html.Table:
    """Create a styled HTML table given headers and row data."""
    # Header row
    header_row = html.Tr([html.Th(col, 
                                  style={"textAlign": "center", "padding": "10px"}) for col in headers])

    # Data rows
    data_rows = []
    for row in rows:

        row_cells = []
        for cell in row:
            if isinstance(cell, str) and cell.startswith("http"):
                # Center image cell
                row_cells.append(
                    html.Td(html.Img(src=cell, 
                                     style={"maxHeight": "50px",     # Limits height
                                            "maxWidth": "100px",     # Limits width
                                            "objectFit": "contain",  # Keeps aspect ratio
                                            "borderRadius": "6px"
                                     }), 
                            style={"textAlign": "center", "padding": "10px"})
                )
            else:
                # Center regular cell
                row_cells.append(html.Td(cell, 
                                         style={"textAlign": "center", "padding": "10px"}))
        data_rows.append(html.Tr(row_cells))

    # Return full table
    return html.Table(
        [header_row] + data_rows,
        style={"width": "100%",
               "border": "1px solid #ccc",
               "borderCollapse": "collapse",
               "backgroundColor": "#f9f9f9",
               "textAlign": "left",
               "padding": "8px"
        }
    )
