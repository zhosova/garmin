import pandas as pd
from dash import Dash
from dash import html
from dash import dcc
import plotly.express as px
from dash import Output, Input

df = pd.read_csv(r"C:\Users\zuzka\OneDrive\Plocha\garmin\Activities.csv")
df[["Čas"]] = df[["Čas"]].apply(pd.to_datetime)

garmin2 = Dash(__name__)

garmin2.layout = html.Header(
    [
        html.H1("Garmin dashboard"),
        html.P("1st attempt."),
        html.Div(
            [
            html.Label("Typ aktivity: "),
            dcc.Dropdown(
                id="Typ_aktivity",
                options=[{"label": data, "value": data
                    } for data in df["Typ aktivity"].unique()
                ],
                    #className="dropdown"
                    
                ),
                html.Label("Vzdálenost: "),
                dcc.Dropdown(
                    id="Vzdalenost",
                    options=[{"label": data, "value": data
                        } for data in range(int(df.Vzdálenost.min()), int(df.Vzdálenost.max())+1)],
                    #className="dropdown"
                )
            ]

        ),
        html.Div(
            dcc.Graph(id="graf"), #className="chart"
            ),
        html.Div(
            [
            html.Label("Tep: "),
            dcc.Slider(
                id="avg_tep",
                min=df["Průměrný ST"].min(),
                max=df["Průměrný ST"].max(),
                step=1,
                value=df["Průměrný ST"].median(),
                marks={tep: str(tep) for tep in range(df["Průměrný ST"].min(), df["Průměrný ST"].max()+1)}
            )
            ])
])
    

@garmin2.callback(
        Output("graf", "figure"),
        Input("Typ_aktivity", "value"),
        Input("avg_tep", "value"),
        Input("Vzdalenost", "value")
             
)
def aktualizuj_graf(Typ_aktivity, Vzdalenost, avg_tep):
    
    vyfiltrovany_df = df

    
    if Typ_aktivity:
        vyfiltrovany_df = vyfiltrovany_df[vyfiltrovany_df["Typ aktivity"] == Typ_aktivity]
    
    #if Vzdalenost:
     #   vyfiltrovany_df = vyfiltrovany_df[vyfiltrovany_df["Vzdálenost"] == Vzdalenost]
    
    data_grafu = px.scatter( #figure
        vyfiltrovany_df,
        x="Datum", #hruby domaci produkt
        y="Čas",
        color="Maximální teplota",
        size="Vzdálenost"
        
               
    ) 

    data_grafu.update_layout(
        plot_bgcolor="#B7CEEC",
        paper_bgcolor="#045F5F",
        font_color="#B7CEEC"
    )

    return data_grafu

if __name__ == "__main__":
    garmin2.run_server(debug=True, port=9052)
