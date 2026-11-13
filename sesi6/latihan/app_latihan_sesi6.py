# sesi6/latihan/app_latihan_sesi6.py — menampilkan keempat jawaban latihan Sesi 6 di Dash
# Jalankan: python sesi6/latihan/app_latihan_sesi6.py  -> buka http://127.0.0.1:8051
from dash import Dash, html, dcc
from latihan_sesi6 import load, buat_figur       # file ada di folder yang sama

figs = buat_figur(load())

app = Dash(__name__, title="Latihan Sesi 6")
app.layout = html.Div(style={"maxWidth": "1200px", "margin": "auto", "fontFamily": "Arial"}, children=[
    html.H1("Latihan Mandiri Sesi 6"),
    html.P("Bar horizontal, bubble chart, sunburst, dan gauge."),
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "12px"},
             children=[dcc.Graph(figure=f) for f in figs.values()]),
])

if __name__ == "__main__":
    app.run(debug=True, port=8051)
