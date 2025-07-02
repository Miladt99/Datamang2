import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

class DatenLoader:
    def __init__(self, dateiname):
        self.dateiname = dateiname
        self.df = None

    def lade_daten(self):
        self.df = pd.read_csv(self.dateiname, parse_dates=["Zeitstempel"])
        return self.df

class KPIs:
    def __init__(self, df):
        self.df = df

    def berechne_kpis(self):
        gesamt_stueckzahl = self.df["Stückzahl"].sum()
        ausschuss = self.df["Ausschuss"].sum()
        ausschussrate = round((ausschuss / gesamt_stueckzahl) * 100, 2)
        return gesamt_stueckzahl, ausschussrate

class Diagramme:
    def __init__(self, df):
        self.df = df

    def stueckzahl_pro_maschine(self):
        return px.bar(
            self.df.groupby("Maschine")["Stückzahl"].sum().reset_index(),
            x="Maschine", y="Stückzahl",
            title="Stückzahl pro Maschine"
        )

    def produktverteilung(self):
        return px.pie(
            self.df, names="Produkt", values="Stückzahl",
            title="Produktverteilung"
        )

    def stueckzahl_ueber_zeit(self):
        return px.line(
            self.df.sort_values("Zeitstempel"),
            x="Zeitstempel", y="Stückzahl",
            title="Stückzahl über Zeit", markers=True
        )
        
    def ausschuss_ueber_zeit(self):
        return px.line(
            self.df.sort_values("Zeitstempel"),
            x="Zeitstempel", y="Ausschuss",
            title="Ausschuss über Zeit", markers=True
        )
        def forecast_vs_actual(self):
        df_sorted = self.df.sort_values("Zeitstempel").copy()
        df_sorted["Forecast"] = (
            df_sorted["Stückzahl"].rolling(window=3, min_periods=1).mean().shift(1)
        )
        fig = px.line(
            df_sorted,
            x="Zeitstempel",
            y=["Stückzahl", "Forecast"],
            title="Forecasted Demand vs. Actual Sales",
            markers=True,
        )
        fig.update_layout(yaxis_title="Stückzahl")
        return fig
    

class ProduktionsDashboard:
    def __init__(self, dateiname):
        self.dateiname = dateiname
        self.app = dash.Dash(__name__)
        self.app.title = "Produktionsdashboard"
        self.df = None
        self.kpi = None
        self.charts = None

    def vorbereiten(self):
        loader = DatenLoader(self.dateiname)
        self.df = loader.lade_daten()

        self.kpi = KPIs(self.df)
        self.charts = Diagramme(self.df)

    def layout_erstellen(self):
        gesamt_stueckzahl, ausschussrate = self.kpi.berechne_kpis()

        self.app.layout = html.Div([
            html.H1("Produktionsdashboard", style={'textAlign': 'center'}),

            # KPIs
            html.Div([
                html.Div([
                    html.H3("Gesamtstückzahl"),
                    html.P(f"{gesamt_stueckzahl}")
                ], style={'width': '30%', 'display': 'inline-block'}),

                html.Div([
                    html.H3("Ausschussrate (%)"),
                    html.P(f"{ausschussrate}")
                ], style={'width': '30%', 'display': 'inline-block'}),
            ], style={'textAlign': 'center'}),

            # Charts
            html.Div([
                dcc.Graph(figure=self.charts.stueckzahl_pro_maschine()),
                dcc.Graph(figure=self.charts.produktverteilung()),
                dcc.Graph(figure=self.charts.stueckzahl_ueber_zeit()),
                dcc.Graph(figure=self.charts.ausschuss_ueber_zeit()),
                dcc.Graph(figure=self.charts.forecast_vs_actual())
            ])
        ])

    def starten(self):
        self.vorbereiten()
        self.layout_erstellen()
        self.app.run(debug=False)

# Main
if __name__ == "__main__":
    dashboard = ProduktionsDashboard("produktionsdaten.csv")
    dashboard.starten()
