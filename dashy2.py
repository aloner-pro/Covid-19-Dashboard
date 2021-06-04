import csv
import numpy as np
from plotly import graph_objs as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'dnhcovid - dnhcovid.csv')

with open(my_file, 'r') as d:
    td = list(csv.reader(d))

date, conf, rec, test, cont, vac, acti, date2, rt, rat, test2, rtp, ratp, tp = [], [], [], [], [], [], [], [], [], [], [], [], [], []

for i in range(1, len(td)):
    if td[i][0] == '17-04-2021':
        break
    else:
        date2 += [td[i][0]]
        rtp += [int(td[i][1])]
        ratp += [int(td[i][2])]
        tp += [int(td[i][3])]
        rt += [int(td[i][8])]
        rat += [int(td[i][9])]
        test2 += [int(td[i][10])]


def zero(num):
    if td[i][num] == '':
        td[i][num] = 0


for i in range(1, len(td)):
    zero(3)
    zero(4)
    zero(5)
    zero(6)
    zero(10)
    zero(11)
    date += [td[i][0]]
    conf += [int(td[i][3])]
    rec += [int(td[i][4])]
    cont += [int(td[i][5])]
    vac += [int(td[i][6])]
    test += [int(td[i][10])]
    acti += [int(td[i][11])]


def zero_to_nan(values):
    val = np.array(values, dtype=np.double)
    val[ val==0 ] = np.nan
    return val


confi = zero_to_nan(conf[::-1])
reco = zero_to_nan(rec[::-1])
conti = zero_to_nan(cont[::-1])
tests = zero_to_nan(test[::-1])
vax = zero_to_nan(vac[::-1])
acto = zero_to_nan(acti[::-1])

# fig = make_subplots(rows=1, cols=2,specs=[[{'type': 'Scattergeo'}, {'type': 'Scatter'}]])
fig = go.Figure()
# fig.add_trace(go.Scattergeo(lat=[27.1751],lon=[78.0421]), row=1, col=1)
fig.add_trace(go.Scatter(x=date[::-1], y=reco, name='Recovered'))
fig.add_trace(go.Scatter(x=date[::-1], y=confi, name='Confirmed '))
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True)
fig.update_layout(paper_bgcolor="LightSteelBlue", font_family="Courier New", hovermode="x unified",
                  title={
                      'text': "Daily Covid Positive & Recovered cases in D&NH",
                      'y': 0.9,
                      'x': 0.5,
                      'xanchor': 'center',
                      'yanchor': 'top'},
                  xaxis_title="Date", yaxis_title="Cases",
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

fig1 = make_subplots(rows=2, cols=2, shared_xaxes=True,
                     specs=[[{"rowspan": 2}, {}],
                            [None, {}]],
                     subplot_titles=("Active Cases", "Daily Tests", "Daily Vaccinations"))
fig1.add_trace(go.Scatter(x=date[::-1], y=tests, mode='lines+markers', name='Tests', line=dict(color="#00f731"),
                          hovertemplate='<b>Date</b>:%{x}<br><b>Tests</b>:%{y}'), row=1, col=2)
fig1.add_trace(go.Bar(x=date[::-1], y=tests, marker_color='#b5f5c2', showlegend=False, hoverinfo="none"), row=1, col=2)
fig1.add_trace(go.Scatter(x=date[::-1], y=acto, mode='lines+markers', name='Active Cases', line=dict(color='#e34a40'),
                          hovertemplate='<b>Date</b>:%{x}<br><b>Active Cases</b>:%{y}'), row=1, col=1)
fig1.add_trace(go.Bar(x=date[::-1], y=acto, marker_color='#ffa07a', showlegend=False, hoverinfo="none"), row=1, col=1)
fig1.add_trace(go.Scatter(x=date[::-1], y=vax, mode='lines+markers', name='Vaccinations', line=dict(color='#3978ed'),
                          hovertemplate='<b>Date</b>:%{x}<br><b>Vaccinations</b>:%{y}'), row=2, col=2)
fig1.add_trace(go.Bar(x=date[::-1], y=vax, marker_color='#63f5f7', showlegend=False, hoverinfo="none"), row=2, col=2)
fig1.update_xaxes(fixedrange=True)
fig1.update_yaxes(fixedrange=True)
fig1.update_layout(
    font_family="Courier New",
    height=500,
    paper_bgcolor="LightSteelBlue")

fig2 = make_subplots(rows=1, cols=2, subplot_titles=("Confirmed Positive Data of D&NH", "Test Data of D&NH"))
fig2.append_trace(go.Bar(x=date2[::-1], y=rtp[::-1], name='RT-PCR +ve'), row=1, col=1)
fig2.append_trace(go.Bar(x=date2[::-1], y=ratp[::-1], name='Rapid Antigen +ve'), row=1, col=1)
fig2.append_trace(go.Bar(x=date2[::-1], y=tp[::-1], name='Total +ve'), row=1, col=1)

fig2.append_trace(go.Bar(x=date2[::-1], y=rt[::-1], name='RT-PCR'), row=1, col=2)
fig2.append_trace(go.Bar(x=date2[::-1], y=rat[::-1], name='Rapid Antigen'), row=1, col=2)
fig2.append_trace(go.Bar(x=date2[::-1], y=test2[::-1], name='Total Tests'), row=1, col=2)
fig2.update_xaxes(fixedrange=True)
fig2.update_yaxes(fixedrange=True)
fig2.update_layout(paper_bgcolor="LightSteelBlue", font_family="Courier New", barmode='stack', hovermode="x unified",
                   title={
                       'text': "Multiple Test Data of D&NH",
                       'y': 0.9,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                   yaxis_title='Numbers',
                   legend_title="Contents")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'D&NH Covid-19| Dashboard'
app.layout = html.Div(children=[
    html.Div([
        html.H2(children='Dadra & Nagar Haveli Covid-19 Analysis', style={"text-align": "center", "color": "red"}),
        html.Label(['Made with ❤️ by - ', html.A('Sohel Ahmed', href='https://github.com/aloner-pro'), 
                    ' & ', html.A('Ritesh Prasad', href="https://covidfacility.dddgov.in/")],
                   style={"text-align": "center"}),
        html.Label([html.A('Covid Bed Facility Portal', href="https://covidfacility.dddgov.in/")],
                   style={"text-align": "center"}),
        html.H6(['* Daily Updated'], style={"text-align": "right", "color": "red"}),
        dcc.Graph(
            id='graph1',
            figure=fig
        ),
    ]),
    html.Div([
        dcc.Graph(
            id='graph2',
            figure=fig1
        ),
    ]),
    html.Div([
        dcc.Graph(
            id='graph3',
            figure=fig2
        ),
        html.Label([html.A('Data Source', href="https://dnh.gov.in/category/press-release/")],
                   style={"text-align": "center"}),
    ]),
])

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
