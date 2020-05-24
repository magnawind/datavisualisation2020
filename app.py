import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import csv

labels = {}
index = 0
sources = []
targets = []
values = []
edge_colors = []

def create_chart(file):
    with open(file, newline='') as csvfile:
        LCAreader = csv.reader(csvfile)
        for row in LCAreader:
            source = row[0]
            target = row[1]
            edge_color = row[2]
            value = row[3]
            if source not in labels:
                labels[source] = index
                index += 1
            if target not in labels:
                labels[target] = index
                index += 1
            sources.append(labels[source])
            targets.append(labels[target])
            values.append(float(value))
            if edge_color == 'red':
                edge_colors.append('rgba(255,0,0, 0.5)')
            elif edge_color == 'blue':
                edge_colors.append('rgba(0,0,255, 0.5)')
            elif edge_color == 'orange':
                edge_colors.append('rgba(150,150,150, 0.5)')

    fig = go.Figure(data=[go.Sankey(
        arrangement = "snap",
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = list(labels.keys()),
          color = "red"
        ),
        link = dict(
          source = sources, # indices correspond to labels, eg A1, A2, A2, B1, ...
          target = targets,
          value = values,
          color = edge_colors
      ))])

    fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
    return fig



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
fig = create_chart('LSA.csv')

app.layout = html.Div([
    html.H2('Magnus Winding'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['Trout', 'Bread', 'Chicken']],
        value='Trout'
    ),
    html.Div(id='display-value'),
    dcc.Graph(id='sankey', figure=fig)
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

@app.callback(dash.dependencies.Output('sankey', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def change_chart(value):
    if value == 'Trout':
        return create_chart('LSA.csv')
    if value == 'Bread':
        return create_chart('LSA2.csv')
    return

if __name__ == '__main__':
    app.run_server(debug=True)