from dash import Dash, html, dcc, Input, Output, ALL, Patch, callback
import dash_cytoscape as cyto
import pandas as pd
import random

app = Dash(__name__)

df_node = pd.read_csv('./df_node.csv')
df_edge = pd.read_csv('./df_edge.csv')

nodes = [
    {
        'data': {'id': id_, 'label': node_},
        'position': {'x': pose_x, 'y': pose_y}
    }
    for id_, node_, pose_x, pose_y in zip(df_node['ID'], df_node['Term'], [random.randint(10, 100) for i in range(len(df_node))], [random.randint(10, 100) for j in range(len(df_node))])
]

edges = [
    {
    	'data': {'source': so, 'target': tar}
    }
    for so, tar in zip(df_edge['source'], df_edge['target'])
]

elements = nodes + edges

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        style={'width': '100%', 'height': '1000px'},
        layout={
            'name': 'random'
        }
    )
])

if __name__ == '__main__':
    app.run(debug=True)