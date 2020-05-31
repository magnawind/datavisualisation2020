import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import csv
import base64


def create_chart(file):

    labels = {}
    label_color = {}
    index = 0
    sources = []
    targets = []
    values = []
    edge_names = []
    edge_colors = []

    with open(file, newline='') as csvfile:
        LCAreader = csv.reader(csvfile)
        for row in LCAreader:
            source = row[0]
            target = row[1]
            edge_name = row[2]
            edge_type = row[3]
            value = row[4]
            node_type = row[5]
            print('node_type', node_type)

            if node_type == 'fossil fuel':
                node_color = 'rgba(197,166,70, 0.5)'
            if node_type == 'process':
                node_color = 'rgba(100,100,100, 0.5)'
            if node_type == 'chemical':
                node_color = 'rgba(255,140,0, 0.5)'

            if source not in label_color:
                label_color[source] = node_color

            if source not in labels:
                labels[source] = index
                index += 1
            if target not in labels:
                labels[target] = index
                index += 1

            sources.append(labels[source])
            targets.append(labels[target])
            values.append(float(value))
            edge_names.append(edge_name)
            if edge_type == 'fossil fuel':
                edge_colors.append('rgba(197, 166, 70, 0.5)')
            elif edge_type == 'natural resource':
                edge_colors.append('rgba(200,200,200, 0.5)')
            elif edge_type == 'product':
                edge_colors.append('rgba(200,200,200, 0.5)')
            elif edge_type == 'chemical':
                edge_colors.append('rgba(255,140,0, 0.5)')
            elif edge_type == 'heat':
                edge_colors.append('rgba(188,47,38, 0.5)')
            elif edge_type == 'electricity':
                edge_colors.append('rgba(125, 249, 255, 0.5)')
            elif edge_type == 'process':
                edge_colors.append('rgba(100,100,100, 0.5)')
            else:
                edge_colors.append('rgba(150,150,150, 0.5)')

    label_list = list(labels.keys())
    label_color_list = [label_color[label] if label in label_color else 'green' for label in label_list]

    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label_list,
            color=label_color_list
        ),
        link=dict(
            source=sources,  # indices correspond to labels, eg A1, A2, A2, B1, ...
            target=targets,
            value=values,
            color=edge_colors,
            label=edge_names
        ))])

    fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
    return fig


def show_orig_image(file):
    encoded_image = base64.b64encode(open(file, 'rb').read())
    return encoded_image


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
fig = create_chart('LCA.csv')
img = show_orig_image('original_trout.png')
encoded_image = base64.b64encode(open(img, 'rb').read())

app.layout = html.Div([
    html.H2('Magnus Winding'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['Trout', 'Bread', 'Chicken']],
        value='Trout'
    ),
    html.Div(id='display-value'),
    dcc.Graph(id='sankey', figure=fig),
    html.Img(id='img', src='data:image/png;base64,{}'.format(encoded_image))
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

@app.callback(dash.dependencies.Output('sankey', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def change_chart(value):
    if value == 'Trout':
        return create_chart('trout_production_chain.csv')
    if value == 'Bread':
        return create_chart('bread_production_chain.csv')
    return


if __name__ == '__main__':
    app.run_server(debug=True)