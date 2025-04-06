import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def plotPairPlots(df, num_cols, color):
    #num_cols = df.select_dtypes(include = ["number"]).columns.tolist()
    df[None] = None
    fig = go.Figure(data = px.scatter_matrix(df[num_cols],
                                             color = df[color],
                                             dimensions = num_cols,
                                             width = 1000, height = 1000)
    )
    return fig

def plotHeatMap(df):
    num_cols = df.select_dtypes(include = ["number"]).columns.tolist()
    correlation_matrix = df[num_cols].corr()
    fig = go.Figure(data = px.imshow(correlation_matrix,
                                     color_continuous_scale = "Inferno",
                                     text_auto = ".3f",
                                     width = 1000, height = 1000)
    )
    return fig
