import numpy as np
import pandas as pd
from dash import Dash
from dash import html
from dash import dcc
import plotly.express as px
from dash import Output, Input

df = pd.read_csv(r"C:\Users\zuzka\OneDrive\Plocha\garmin\Activities.csv")

garmin2 = Dash(__name__)

garmin2.layout = html.Div(
    [
        html.H1("Garmin dashboard"),
        html.P("1st attempt."),
        html.Div(
            [
                html.Label("Typ aktivity: "),
                dcc.Dropdown(
                    id="Typ_aktivitky",
                    options=[ {"label": data,"value": data} for data in df["Typ aktivity"].unique() ],
                ),
            ]

        ),
        html.Div(dcc.Graph(id="graf")),
        html.Div(
            [
            html.Label("Max tep "),
            dcc.Slider(
                id="max_tep",
                min=df["Maximální ST"].min(),
                max=df["Maximální ST"].max(),
                step=1,
                value=df["Maximální ST"].min(),
                marks={rok: str(rok) for rok in range(df["Maximální ST"].min(), df["Maximální ST"].max()+1)}
            )
            ])
    ]
)

@garmin2.callback(
        Output("graf", "figure"),
        Input("Typ_aktivitky", "value"),
        Input("max_tep", "value")
             
)
def aktualizuj_graf(Typ_aktivitky, max_tep):
    
    data_grafu = px.scatter( #figure
        df,
        x="Vzdálenost", #hruby domaci produkt
        y="Čas",
        size="Průměrný ST",
               
    ) 

    data_grafu.update_layout(
        plot_bgcolor="#011833",
        paper_bgcolor="#011833",
        font_color="#7FDBFF"
    )

    return data_grafu

if __name__ == "__main__":
    garmin2.run_server(debug=True, port=9050)