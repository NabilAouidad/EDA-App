import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from distributions import plotHistograms, plotBoxes, plotBars
from correlations import plotPairPlots, plotHeatMap
from scipy.stats import zscore
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
st.set_page_config(layout = "wide", page_title = "Data Cleaning Toolkit")

style = """
    <style>
    button[data-baseweb="tab"] {
        margin: 0 auto;
    }

    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.3rem;
    }
    </style>
    """

st.markdown(style, unsafe_allow_html = True)

container = st.container(height = 125, border = False)
container.write('<h1 style="text-align: center;">Data Cleaning Toolkit</h1>', 
         unsafe_allow_html=True)

st.empty()

st.markdown("-------------------")

#-----------------------------------------------------------

def extractNumCols(df):
    return df.select_dtypes(include = ["number"]).columns.tolist()

def extractObjCols(df):
    return df.select_dtypes(include = ["object"]).columns.tolist()

def showDataInfo(df):
    shapeCol, featuresCol, numFeaturesCol, objFeaturesCol = st.columns([1, 1, 1, 1])

    shapeCol.markdown("### Shape")
    shapeCol.markdown(f"***Rows*** : {df.shape[0]}")
    shapeCol.markdown(f"***Columns*** : {df.shape[1]}")

    featuresCol.markdown("### Features")
    featuresCol.dataframe(pd.DataFrame({"Features":df.columns.tolist()},
                                       index = range(1, len(df.columns)+1)))
    
    numFeaturesCol.markdown("### Numerical")
    numFeaturesCol.dataframe(pd.DataFrame({"Features":extractNumCols(df)},
                                          index = range(1, len(extractNumCols(df))+1)))
    
    objFeaturesCol.markdown("### Object")
    objFeaturesCol.dataframe(pd.DataFrame({"Features":extractObjCols(df)},
                                          index = range(1, len(extractObjCols(df))+1)))
    
    st.markdown("### Descriptive Statistics")
    st.dataframe(df.describe(include = "all"))

    st.markdown("### Data Sample")
    st.dataframe(df.sample(len(df)//10))

def plotMissingData(df):
    missingData = df.isnull().sum()
    figure = px.bar(x = missingData.index, y = missingData.values,
                orientation = 'v', labels = {'x':"Feature", 'y':"Missing Records"},
                title = "Missing data representation of the dataset")
    figure.update_layout(width = 750, title_x = 0.5)
    return figure

def showDuplicates(df):
     return st.dataframe(df.duplicated())

def extractOutliersZScore(df):
    num_cols = extractNumCols(df)
    z_scores = df[num_cols].apply(zscore)
    outliers_z = (z_scores.abs()>3).any(axis = 1)
    return pd.DataFrame(df[outliers_z])

def extractOutliersIQR(df):
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3-Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers_iqr = ((df < lower_bound) | (df > upper_bound)).any(axis=1)

    return pd.DataFrame(df[outliers_iqr])

st.sidebar.markdown("# Options")
uploaded_file = st.sidebar.file_uploader("Upload your data file", type = ["csv"])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        st.sidebar.info("Only CSV files are supported!")

    mainBox = st.sidebar.selectbox(label = " ", 
                                   options = ["About the dataset", "Data Quality", "Data Distributions",
                                              "Correlations", "Group By"])
    match mainBox:

        case "About the dataset":
            showDataInfo(df)

        case "Data Quality":
            dataQualityBox = st.selectbox(label = "Select the data quality issue you want to check for", 
                                          options = ["Duplicates", "Missing Data", "Outliers"], 
                                          index = None)
            
            match dataQualityBox:
                case "Duplicates":
                    showDuplicates(df)
                case "Missing Data":
                    st.dataframe(pd.DataFrame(df.isnull().sum(), columns = ["Count"]))
                    st.plotly_chart(plotMissingData(df))
                case "Outliers":
                    st.plotly_chart(plotHistograms(df))
                    st.plotly_chart(plotBoxes(df))
                    outliersBox = st.selectbox(label = "Choose the method you want to use int order to retrieve the list of the outliers", 
                                               options = ["Z Score", "Interquantile Range"], 
                                               index = None)
                    match outliersBox:
                        case "Z Score":
                            st.dataframe(extractOutliersZScore(df))
                        case "Interquantile Range":
                            st.dataframe(extractOutliersIQR(df))
        
        case "Data Distributions":
            try:
                st.plotly_chart(plotHistograms(df))
                st.plotly_chart(plotBars(df))
            except (IndexError, ZeroDivisionError) as e:
                st.empty()

        case "Correlations":
            col1, col2 = st.columns(2)
            num_cols = col1.multiselect(label = "Select the numerical features to plot the correlations map",
                                        options = extractNumCols(df))
            color = col2.selectbox(label = "Color", options = extractObjCols(df), index = None)
            
            st.plotly_chart(plotPairPlots(df, num_cols, color))
            st.plotly_chart(plotHeatMap(df[num_cols]))

        case "Group By":
            col1, col2, col3 = st.columns(3)

            num_cols = col1.multiselect(label = "Feature selection", options = extractNumCols(df))
            obj_col = col3.selectbox(label = "Group by", options = extractObjCols(df), index = None)
            stat = col2.selectbox(label = "Statistic", options = ["Mean", "Median", "Sum"])

            if None in [num_cols, obj_col]:
                pass

            else:
                match stat:
                    case "Mean":   
                        df_grouped = df.groupby(obj_col)[num_cols].mean().reset_index()
                    case "Median":
                        df_grouped = df.groupby(obj_col)[num_cols].median().reset_index()
                    case "Sum":
                        df_grouped = df.groupby(obj_col)[num_cols].sum().reset_index()
                traces = []
                for col in num_cols:
                    trace = go.Bar(x = df_grouped[obj_col], y = df_grouped[col], name = col)
                    traces.append(trace)
                fig = go.Figure(data = traces)
                fig.update_layout(
                    xaxis_title = obj_col,
                    barmode = "group",
                    template = "plotly_white"
                )
                st.plotly_chart(fig)