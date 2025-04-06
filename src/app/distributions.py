import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.colors import qualitative

def numberFactoring(number):
    factor_pairs = []
    for i in range(1, int(number**0.5)+1):
        if number%i == 0:
            factor_pairs.append((i, number//i))
    return factor_pairs

def isPrime(number):
    if number < 2:
        return False
    for i in range(2, number//2+1):
        if number % i == 0:
            return False
    return True

def plotBars(df):
    obj_cols = df.select_dtypes(include = ["object"]).columns.tolist()
    num_frames = len(obj_cols)

    if isPrime(num_frames):
        num_frames = num_frames+1

    color_pallette = qualitative.Dark24
    num_colors = len(color_pallette)

    n_rows, n_cols = numberFactoring(num_frames)[-1][0], numberFactoring(num_frames)[-1][1]
    c = 0
    fig = make_subplots(rows = n_rows, cols = n_cols,
                        column_widths = [1000 for i in range(n_cols)], 
                        row_heights = [1000 for i in range(n_rows)],
                        horizontal_spacing = 1/(num_frames-1), vertical_spacing = 0.17)
    fig.update_layout({"height":900, "width":900})

    for i in range(1, n_rows+1):
        for j in range(1, n_cols+1):
            if i*j > len(obj_cols):
                break
            else :
                count = df[obj_cols[c]].value_counts().sort_values().head(10)
                fig.add_trace(go.Bar(y = count.values, x = count.index,
                                      orientation = 'v', marker = {"color":color_pallette[c%num_colors]},
                                      name = obj_cols[c]), row = i, col = j)
                c += 1
    fig.update_layout({"title":"Categories"})
    return fig

def plotHistograms(df):
    num_cols = df.select_dtypes(include = ["number"]).columns.tolist()
    num_frames = len(num_cols)

    if isPrime(num_frames):
        num_frames = num_frames+1

    color_pallette = qualitative.Dark24
    num_colors = len(color_pallette)

    n_rows, n_cols = numberFactoring(num_frames)[-1][0], numberFactoring(num_frames)[-1][1]

    c = 0
    fig = make_subplots(rows = n_rows, cols = n_cols,
                        column_widths = [1000 for i in range(n_cols)], 
                        row_heights = [1000 for i in range(n_rows)],
                        horizontal_spacing = 1/(num_frames-1), vertical_spacing = 0.17)
    fig.update_layout({"height":900, "width":900})
    
    for i in range(1, n_rows+1):
        for j in range(1, n_cols+1):
            if i*j > len(num_cols):
                break
            else :
                fig.add_trace(go.Histogram(x = df[num_cols[c]],
                                       histfunc = "count",
                                       name = num_cols[c], marker = {"color":color_pallette[c%num_colors]},
                                       nbinsx = 20),
                                       row = i, col = j)
                c += 1
    fig.update_layout({"title":"Histograms of Numerical Data"})
    return fig

def plotBoxes(df):
    num_cols = df.select_dtypes(include = ["number"]).columns.tolist()
    num_frames = len(num_cols)

    if isPrime(num_frames):
        num_frames = num_frames+1

    color_pallette = qualitative.Dark24
    num_colors = len(color_pallette)

    n_rows, n_cols = numberFactoring(num_frames)[-1][0], numberFactoring(num_frames)[-1][1]

    c = 0
    fig = make_subplots(rows = n_rows, cols = n_cols,
                        column_widths = [1000 for i in range(n_cols)], 
                        row_heights = [1000 for i in range(n_rows)],
                        horizontal_spacing = 0.13, vertical_spacing = 0.17)
    fig.update_layout({"height":900, "width":900})
    
    for i in range(1, n_rows+1):
        for j in range(1, n_cols+1):
            if i*j > len(num_cols):
                break
            else :
                fig.add_trace(go.Box(y = df[num_cols[c]],
                                     boxmean = True,
                                     name = num_cols[c], marker = {"color":color_pallette[c%num_colors]}
                                    ),row = i, col = j)
                c += 1
    fig.update_layout({"title":"Box Plots of Numerical Data"})
    return fig