import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import os

# Load dataset
df = pd.read_csv("universal_top_spotify_songs.csv")

# Clean & prep columns
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df['snapshot_date'] = pd.to_datetime(df['snapshot_date'], errors='coerce')
df['year'] = df['snapshot_date'].dt.year
df['month'] = df['snapshot_date'].dt.month

# Audio features to analyze
audio_features = [
    'danceability', 'energy', 'acousticness', 'instrumentalness', 'liveness',
    'valence', 'tempo', 'speechiness', 'loudness', 'duration_ms'
]

# Get top unique artists/songs
df['artists'] = df['artists'].astype(str)
df['track_id'] = df['name'].astype(str)
top_artists = df['artists'].dropna().unique()
top_tracks = df['track_id'].dropna().unique()

px.set_mapbox_access_token(open(".mapbox_token").read())

# Dash app setup with external CSS
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
    ]
)
app.title = "Spotify Unwrapped"

# Load your custom CSS
app.css.append_css({
    "external_url": "/assets/style.css"  # Make sure to create an assets folder
})

# App layout with Spotify-style design
app.layout = html.Div([
    # DLSU Logo Overlay
    html.Div(
        html.Img(
            src="assets/De_La_Salle_University_Seal.png",
            className="dlsu-corner-logo"
        ),
        className="dlsu-logo-overlay"
    ),
    
    # Sidebar
    html.Div(
        [
            html.Div(
                [
                    # Logo
                    html.Div(
                        html.Img(
                            src="assets/Spotify Unwrapped.png",
                            className="spotify-logo"
                        ),
                        className="logo-container",
                        style={'maxWidth': '100%', 'maxHeight': '100%'}
                    ),
                    
                    # Menu Items
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.A(
                                        [
                                            html.I(className="fas fa-search"),
                                            html.Span("Search", className="menu-text")
                                        ],
                                        href="#search", 
                                        className="menu-item"
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    html.A(
                                        [
                                            html.I(className="fa fa-globe"),
                                            html.Span("Region", className="menu-text")
                                        ],
                                        href="#region", 
                                        className="menu-item"
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    html.A(
                                        [
                                            html.I(className="far fa-star"),
                                            html.Span("Popularity", className="menu-text")
                                        ],
                                        href="#popularity",  
                                        className="menu-item"
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    html.A(
                                        [
                                            html.I(className="fas fa-chart-bar"),
                                            html.Span("Feature", className="menu-text")
                                        ],
                                        href="#feature", 
                                        className="menu-item"
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    html.A(
                                        [
                                            html.I(className="fas fa-chart-line"),
                                            html.Span("Correlation", className="menu-text")
                                        ],
                                        href="#scatter", 
                                        className="menu-item"
                                    ),
                                ]
                            ),
                        ],
                        className="sidebar-menu"
                    ),
                    
                    # Playlists Image
                    html.Div(
                        html.Img(
                            src="assets/Side_bar.png",
                            className="sidebar-image",
                            style={'width': '50%'}
                        ),
                        className="sidebar-playlists"
                    )
                ],
                className="sidebar-content"
            )
        ],
        className="sidebar d-none d-md-block"
    ),
    
    # Main Content
    html.Div(
        [
            # Top Navigation
            html.Nav(
                [
                    html.Div(
                        [
                            # Mobile toggle button
                            html.Div(
                                dbc.Button(
                                    html.Span(className="navbar-toggler-icon"),
                                    className="navbar-toggler",
                                    id="navbar-toggler"
                                ),
                                className="d-md-none"
                            ),
                            
                            # Navigation links
                            html.Div(
                                [
                                    html.A(
                                        "Data", 
                                        href="https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated", 
                                        target="_blank",  # Opens in new tab
                                        className="nav-link"
                                    ),
                                    html.A(
                                        "About Us", 
                                        href="#about-section",  # Links to an anchor at your about section
                                        className="nav-link"
                                    ),
                                    html.A(
                                        "LISTEN NOW", 
                                        href="https://open.spotify.com/playlist/37i9dQZF1DZ06evO2G3nP2?si=j3wQ-TjIQ4CW7UBHgDgOVA",  
                                        target="_blank",  # Opens in new tab
                                        className="nav-link listen-btn")
                                ],
                                className="nav-buttons ml-auto"
                            )
                        ],
                        className="container-fluid"
                    )
                ],
                className="navbar navbar-dark"
            ),
            
            # Mobile Navigation (Collapsed)
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.I(className="fas fa-home"),
                                    html.Span("Home")
                                ],
                                className="menu-item active"
                            ),
                            html.Div(
                                [
                                    html.I(className="fas fa-search"),
                                    html.Span("Search")
                                ],
                                className="menu-item"
                            ),
                            html.Div(
                                [
                                    html.I(className="fas fa-book"),
                                    html.Span("Your Library")
                                ],
                                className="menu-item"
                            )
                        ],
                        className="mobile-menu"
                    )
                ],
                className="collapse navbar-collapse d-md-none",
                id="navbarNav"
            ),
            
            # Content Container
            html.Div(
                [
                    # Header Section
                    html.Div(
                        [
                            html.H1("Spotify Unwrapped"),
                            html.H2("Analyzing Trends in Music Popularity and Characteristics",
                                     className="sub-header"),
                            
                            # Problem Statement
                            html.Div(
                                [
                                    html.H3("Problem Statement"),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div(
                                                    html.Img(
                                                        src="assets/Henry_Wadsworth_Longfellow.png",
                                                        className="img-fluid rounded-circle longfellow-img"
                                                    ),
                                                    className="longfellow-container"
                                                ),
                                                width=3, md=2
                                            ),
                                            dbc.Col(
                                                html.P([
                                                    "As Henry Wadsworth Longfellow said, music is a universal language, transcending barriers and "
                                                    "connecting people worldwide. Music trends reflect cultural and technological changes, with new genres "
                                                    "emerging and evolving through digital platforms. What makes a song successful today isn't just radio play— "
                                                    "it's viral moments on platforms like TikTok and Spotify. By understanding these trends, we see how music "
                                                    "shapes and mirrors societal changes, continuing to be a powerful tool for expression and connection.",
                                                    html.Br(),
                                                    html.Br(),
                                                    "• What happens to song popularity over the years? Has it increased or decreased? Why might this be?",
                                                    html.Br(),
                                                    "• How did the popularity of different music genres evolve from 2000 to 2019?",
                                                    html.Br(),
                                                    "• Audio Feature Analysis: What are the average audio feature values (e.g., BPM, energy, danceability)" 
                                                    "  for top songs each year?"
                                                ],className="problem-text"),
                                                width=9, md=10
                                            )
                                        ],
                                        className="align-items-center"
                                    )
                                ],
                                className="problem-statement-container"
                            )
                        ],
                        className="content-section"
                    ),
                    
                    # Controls and Visualizations
                    dbc.Row(
                        [
                            # Controls Column
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H4("Data Controls"),
                                        
                                        # View Type Radio Buttons
                                        html.Div(
                                            [
                                                html.Label("View Type:", className="control-label"),
                                                dbc.RadioItems(
                                                    id='view-radio',
                                                    options=[
                                                        {'label': 'Song', 'value': 'song'},
                                                        {'label': 'Artist', 'value': 'artist'}
                                                    ],
                                                    value='song',
                                                    className="custom-radio",
                                                    label_style={"margin-right": "15px", "color": "#FFFFFF"},  # Correct property for label styling
                                                    input_style={"margin-right": "5px"}  # Correct property for input styling
                                                )
                                            ],
                                            className="control-group",id="search"
                                        ),
                                        
                                        # Entity Dropdown
                                        html.Div(
                                            [
                                                html.Label("Select Song/Artist:", className="control-label"),
                                                dcc.Dropdown(
                                                    id='entity-dropdown',
                                                        style={
                                                            'backgroundColor': '#000000',
                                                            'color': '#FFFFFF'
                                                        }
                                                )
                                            ],
                                            className="control-group"
                                        ),
                                        
                                        # Date Range
                                        html.Div(
                                            [
                                                html.Label("Date Range:", className="control-label"),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dcc.DatePickerSingle(
                                                                id='start-date',
                                                                min_date_allowed=df['snapshot_date'].min(),
                                                                max_date_allowed=df['snapshot_date'].max(),
                                                                initial_visible_month=df['snapshot_date'].min(),
                                                                date=df['snapshot_date'].min(),
                                                                display_format='YYYY-MM-DD'
                                                            ),
                                                            width=5
                                                        ),
                                                        
                                                        # Adding "to" between the start and end dates
                                                        dbc.Col(
                                                            html.Div(
                                                                "to",
                                                                className="control-label text-green"
                                                            ),
                                                            width=2,
                                                            className="d-flex justify-content-center align-items-center"
                                                        ),
                                                        
                                                        dbc.Col(
                                                            dcc.DatePickerSingle(
                                                                id='end-date',
                                                                min_date_allowed=df['snapshot_date'].min(),
                                                                max_date_allowed=df['snapshot_date'].max(),
                                                                initial_visible_month=df['snapshot_date'].max(),
                                                                date=df['snapshot_date'].max(),
                                                                display_format='YYYY-MM-DD'
                                                            ),
                                                            width=5
                                                        )
                                                    ]
                                                )
                                            ],
                                            className="control-group"
                                        ),
                                    ],
                                    className="content-section"
                                ),
                                width=12, md=4
                            ),
                            
                            # Visualizations Column
                            dbc.Col(
                                [
                                    # Choropleth Map
                                    html.Div(
                                        [
                                            html.H4("Global Music Popularity by Region", id="region"),
                                            dcc.Graph(id='choropleth-map', className="visualization-container"),
                                            html.P(
                                                "The choropleth map visualizes popularity across different regions, with darker colors indicating higher popularity.",
                                                className="chart-description"
                                            )
                                        ],
                                        className="content-section"
                                    ),
                                    
                                    # Line Chart
                                    html.Div(
                                        [
                                            html.H4("Popularity Trend Over Time", id="popularity"),
                                            dcc.Graph(id='line-chart', className="visualization-container"),
                                            html.P(
                                                "This line graph tracks how audio features like danceability and energy have changed over time for the selected songs.",
                                                className="chart-description"
                                            )
                                        ],
                                        className="content-section"
                                    )
                                ],
                                #width=12, md=8
                            )
                        ],
                        className="mt-4"
                    ),
                    
                    # Full Width Visualizations
                    html.Div(
                        [
                            # Bar Chart
                            html.Div(
                                [
                                    html.H4("Top Songs by Selected Audio Feature",id="feature"),
                                    # Audio Feature Dropdown
                                            html.Div(
                                                [
                                                    html.Label("Audio Feature:", className="control-label"),
                                                    dcc.Dropdown(
                                                        id='bar-attribute',
                                                        options=[{'label': a, 'value': a} for a in audio_features],
                                                        value='energy',
                                                        style={
                                                                'backgroundColor': '#000000',
                                                                'color': '#FFFFFF'
                                                            }
                                                    )
                                                ],
                                                className="control-group mb-3"
                                            ),
                                    dcc.Graph(id='bar-chart', className="visualization-container"),
                                    html.P(
                                        "This bar chart shows the top songs based on the selected audio feature.",
                                        className="chart-description"
                                    )
                                ],
                                className="content-section"
                            ),
                            
                            # Scatter Plot
                            html.Div(
                                [
                                    html.H4("Song Popularity vs. Audio Features",id="scatter"),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dcc.Dropdown(
                                                    id='x-attribute',
                                                    options=[{'label': a, 'value': a} for a in audio_features],
                                                    value='danceability',
                                                    style={
                                                            'backgroundColor': '#000000',
                                                            'color': '#FFFFFF'
                                                        }
                                                ),
                                                width=6
                                            ),
                                            dbc.Col(
                                                dcc.Dropdown(
                                                    id='y-attribute',
                                                    options=[{'label': a, 'value': a} for a in audio_features],
                                                    value='energy',
                                                    style={
                                                            'backgroundColor': '#000000',
                                                            'color': '#FFFFFF'
                                                        }
                                                ),
                                                width=6
                                            )
                                        ],
                                        className="mb-3"
                                    ),
                                    dcc.Graph(id='scatter-plot', className="visualization-container"),
                                    html.P(
                                        "The scatter plot reveals relationships between different audio features and popularity.",
                                        className="chart-description"
                                    )
                                ],
                                className="content-section"
                            )
                        ]
                    )
                ],
                className="container-fluid content-container"
            )
        ],
        className="main-content"
    ),

    # About US
       
    html.Div(
    [
        html.H2("About the Developers", style={
            "fontSize": "22px",
            "marginBottom": "20px",
            "color": "#1DB954"  # Spotify green for a pop of color
        }),

        html.Ul(
            [
                html.Li("Jonalaine Aporado"),
                html.Li("Edmar Dizon"),
                html.Li("John Carlo Gonzales"),
                html.Li("Tyrone Victor Garcia"),
                html.Li("Vince Jefferson Tadeo"),
                html.Li("Wilson Tang")
            ],
            style={
                "listStyleType": "none",
                "padding": 0,
                "margin": 0,
                "fontSize": "14px",
                "color": "#FFFFFF",
                "lineHeight": "2"
            }
        )
    ],
    id="about-section",
    style={
        "backgroundColor": "#121212",
        "textAlign": "center",
        "padding": "40px 20px",
        "borderTop": "2px solid #1DB954",
        "marginTop": "60px"
    }
),
 
    # Player Bar
    html.Div(
        html.Img(
            src="assets/bottom_pic.png",
            className="img-fluid w-100 h-100"
        ),
        className="player-bar"
    ),
    
    # Footer
    html.Footer(
        html.Div(
            [
                html.Div("© 2024 Spotify Unwrapped. All Rights Reserved.", className="copyright"),
                html.Div(
                    [
                        html.Span("Presented by", className="attribution"),
                        html.Img(
                            src="assets/De_La_Salle_University_Seal.png",
                            className="dlsu-logo-small"
                        )
                    ],
                    className="attribution"
                )
            ],
            className="footer-content container-fluid"
        ),
        className="footer"
    )
])

# Callback functions (same as before)
@app.callback(
    Output('entity-dropdown', 'options'),
    Output('entity-dropdown', 'value'),
    Input('view-radio', 'value')
)
def update_dropdown(view_type):
    if view_type == 'song':
        options = [{'label': name, 'value': name} for name in sorted(top_tracks)]
        return options, options[0]['value']
    else:
        options = [{'label': name, 'value': name} for name in sorted(top_artists)]
        return options, options[0]['value']

@app.callback(
    Output('choropleth-map', 'figure'),
    Output('line-chart', 'figure'),
    Input('view-radio', 'value'),
    Input('entity-dropdown', 'value'),
    Input('start-date', 'date'),
    Input('end-date', 'date')
)
def update_visuals(view, entity, start_date, end_date):
    # Convert string dates to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Filter data by date range
    dff = df[(df['snapshot_date'] >= start_date) & (df['snapshot_date'] <= end_date)]

    if view == 'song':
        dff = dff[dff['track_id'] == entity]
    else:
        dff = dff[dff['artists'] == entity]

    map_fig = px.choropleth(
        dff,
        locations='country',
        locationmode='country names',
        color='popularity',
        color_continuous_scale='cividis',
        hover_name='country',
        title='Popularity by Country'
    )
    map_fig.update_layout(
        paper_bgcolor='#282828', 
        plot_bgcolor='#282828', 
        font_color='#FFFFFF',
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # NEW: Line chart showing daily popularity
    daily_popularity = dff.groupby('snapshot_date')['popularity'].mean().reset_index()
    line_fig = px.line(
        daily_popularity, 
        x='snapshot_date', 
        y='popularity',
        title=f'Daily Popularity Trend for {entity}'
    )
    line_fig.update_layout(
        paper_bgcolor='#282828', 
        plot_bgcolor='#282828', 
        font_color='#FFFFFF',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title='Date',
        yaxis_title='Popularity Score'
    )
    line_fig.update_traces(line_color='#1DB954')  # Spotify green line

    return map_fig, line_fig

@app.callback(
    Output('bar-chart', 'figure'),
    Input('bar-attribute', 'value')
)
def update_bar_chart(attribute):
    # Handle None or invalid attribute
    if attribute is None or attribute not in df.columns:
        # Return empty figure with same styling using px
        fig = px.bar(title="Select an audio feature to display data")
        fig.update_layout(
            paper_bgcolor='#282828',
            plot_bgcolor='#282828',
            font_color='#FFFFFF',
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Feature Value",
            yaxis_title="Song",
            showlegend=False
        )
        # Hide empty axes
        fig.update_xaxes(showgrid=False, visible=False)
        fig.update_yaxes(showgrid=False, visible=False)
        return fig
    
    try:
        # Get top 10 songs by selected attribute
        bar_data = df.groupby('track_id')[attribute].mean().sort_values(ascending=False).head(10).reset_index()
        
        # Create horizontal bar chart
        fig = px.bar(
            bar_data, 
            x=attribute, 
            y='track_id',
            orientation='h',
            title=f"Top Songs by {attribute.capitalize()}",
            color=attribute,
            color_continuous_scale='cividis'
        )
        
        # Update layout
        fig.update_layout(
            paper_bgcolor='#282828', 
            plot_bgcolor='#282828', 
            font_color='#FFFFFF',
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title=attribute.capitalize(),
            yaxis_title="Song",
            yaxis={'categoryorder':'total ascending'},
            coloraxis_showscale=False
        )
        
        # Set y-axis interval to 0.1
        fig.update_xaxes(
            dtick=0.1,
            range=[0, 1] if attribute in ['danceability', 'energy', 'valence'] else None
        )
        
        return fig
    
    except Exception as e:
        # Fallback in case of other errors using px
        print(f"Error generating bar chart: {str(e)}")
        fig = px.bar(title="Error loading chart")
        fig.update_layout(
            paper_bgcolor='#282828',
            plot_bgcolor='#282828',
            font_color='#FFFFFF'
        )
        return fig

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('x-attribute', 'value'),
    Input('y-attribute', 'value')
)
def update_scatter(x_attr, y_attr):
    fig = px.scatter(df, x=x_attr, y=y_attr, color='popularity', color_continuous_scale='cividis',
                     hover_name='artists', 
                     title=f"{x_attr.capitalize()} vs {y_attr.capitalize()}")
    fig.update_layout(
        paper_bgcolor='#282828', 
        plot_bgcolor='#282828', 
        font_color='#FFFFFF',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)