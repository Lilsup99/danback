import plotly.express as px
import plotly.graph_objects as go

from pandas import Series

def grafica_columna(serie:Series):
    if serie.dtype == 'object':
        if len(serie.drop_duplicates())<=15:
            fig = px.bar(serie.value_counts(),x=serie.value_counts().index, y='count')
            return fig
        else:
            fig = go.Figure(go.Indicator(
                            mode = "number",
                            value = len(serie.drop_duplicates()),
                            title = {'text': "Valores unicos", 'font': {'size': 24}},
                            number={'font': {'size': 70}}
                            ))
            fig.update_layout(paper_bgcolor = "rgba(20, 94, 137, 0.2)",font = {'color': "white", 'family': "Arial"})
            return fig
    elif (serie.dtype == 'float64') or (serie.dtype == 'int64'):
        if len(serie.drop_duplicates()) >= 15:
            fig = px.histogram(serie)
            return fig
        else:
            fig = px.bar(serie.value_counts(),x=serie.value_counts().index, y='count')
            return fig