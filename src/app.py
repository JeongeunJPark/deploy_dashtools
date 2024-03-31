import textwrap
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_cytoscape as cyto
import pandas as pd
import random


app = Dash(__name__)
server = app.server

df_node = pd.read_csv('./data/df_node.csv')
df_edge = pd.read_csv('./data/df_edge.csv')
result = pd.read_csv('./data/test.csv')


colors = ['IndianRed', 'LightCoral', 'Salmon', 'DarkSalmon', 'LightSalmon', 'Crimson', 'Red',
          'FireBrick', 'DarkRed', 'Pink', 'LightPink', 'HotPink', 'DeepPink', 'MediumVioletRed',
          'PaleVioletRed', 'LightSalmon', 'Coral', 'Tomato', 'OrangeRed', 'DarkOrange', 'Orange',
          'Gold', 'Yellow', 'LightYellow', 'LemonChiffon', 'LightGoldenrodYellow', 'PapayaWhip',
          'Moccasin', 'PeachPuff', 'PaleGoldenrod', 'Khaki', 'DarkKhaki', 'Lavender', 'Thistle',
          'Plum', 'Violet', 'Orchid', 'Fuchsia', 'Magenta', 'MediumOrchid', 'MediumPurple', 'RebeccaPurple',
          'BlueViolet', 'DarkViolet', 'DarkOrchid', 'DarkMagenta', 'Purple', 'Indigo', 'SlateBlue',
          'DarkSlateBlue', 'MediumSlateBlue', 'GreenYellow', 'Chartreuse', 'LawnGreen', 'Lime', 'LimeGreen',
          'PaleGreen', 'LightGreen', 'MediumSpringGreen', 'SpringGreen', 'MediumSeaGreen', 'SeaGreen',
          'ForestGreen', 'Green', 'DarkGreen', 'YellowGreen', 'OliveDrab', 'Olive', 'DarkOliveGreen',
          'MediumAquamarine', 'DarkSeaGreen', 'LightSeaGreen', 'DarkCyan', 'Teal', 'Aqua', 'Cyan', 'LightCyan',
          'PaleTurquoise', 'Aquamarine', 'Turquoise', 'MediumTurquoise', 'DarkTurquoise', 'CadetBlue', 'SteelBlue',
          'LightSteelBlue', 'PowderBlue', 'LightBlue', 'SkyBlue', 'LightSkyBlue', 'DeepSkyBlue', 'DodgerBlue',
          'CornflowerBlue', 'MediumSlateBlue', 'RoyalBlue', 'Blue', 'MediumBlue', 'DarkBlue', 'Navy', 'MidnightBlue',
          'Cornsilk', 'BlanchedAlmond', 'Bisque', 'NavajoWhite', 'Wheat', 'BurlyWood', 'Tan', 'RosyBrown',
          'SandyBrown', 'Goldenrod', 'DarkGoldenrod', 'Peru', 'Chocolate', 'SaddleBrown', 'Sienna', 'Brown',
          'Maroon', 'White', 'Snow', 'HoneyDew', 'MintCream', 'Azure', 'AliceBlue', 'GhostWhite', 'WhiteSmoke',
          'SeaShell', 'Beige', 'OldLace', 'FloralWhite', 'Ivory', 'AntiqueWhite', 'Linen', 'LavenderBlush',
          'MistyRose', 'Gainsboro', 'LightGray', 'Silver', 'DarkGray', 'Gray', 'DimGray', 'LightSlateGray',
          'SlateGray', 'DarkSlateGray', 'Black']
nodes = [
    {
        'data': {'id': id_name, 'label': term, 'group': group, 'gene': gene, 'size': size},
        'position': {'x': pos_x, 'y': pos_y},
    }
    for id_name, term, group, gene, size, pos_x, pos_y in zip(df_node['ID'], df_node['Term'], df_node['GOGroups'], df_node['Associated Genes Found'], df_node['Term PValue'],
                                                  [random.randint(10, 100) for i in range(len(df_node))],
                                                  [random.randint(10, 100) for j in range(len(df_node))])
]

group_to_color = {
    "Group00": "IndianRed",
    "Group01": "red",
    "Group02": "blue",
    "Group03": "green",
    "Group04": "DarkSalmon",
    "Group05": "Crimson",
    "Group06": "FireBrick",
    "Group07": "DarkRed",
    "Group08": "LightSalmon",
    "Group09": "Coral",
    "Group10": "Tomato",
    "Group11": "Turquoise",
    "Group12": "CadetBlue",
    "Group13": "MediumTurquoise",
    "Group14": "Purple",
    "Group15": "Indigo",
    "Group16": "BlueViolet",
    "Group17": "Cornsilk",
    "Group18": "Goldenrod",
    "Group19": "MintCream",
    "Group20": "MediumSpringGreen",
    "Group21": "SpringGreen",
    "Group22": "MediumSeaGreen",
    "Group23": "SeaGreen",
    "Group24": "DarkGreen",
    "Group25": "YellowGreen",
    "Group26": "OliveDrab",
    "Group27": "Olive",
    "Group28": "LightSteelBlue",
    "Group29": "PowderBlue",
    "Group30": "LightBlue",
    "Group31": "SkyBlue",
    "Group32": "LightSkyBlue",
    "Group33": "DeepSkyBlue",
    "Group34": "DodgerBlue",
    "Group35": "Gold",
    "Group36": "Yellow",
    "Group37": "LightYellow",
    "Group38": "LemonChiffon",
    "Group39": "Moccasin",
    "Group40": "PeachPuff",
    "Group41": "Khaki",
    "Group42": "Lavender",
    "Group43": "Thistle",
    "Group44": "HotPink",
    "Group45": "MediumVioletRed",
}

# 모든 노드를 순회하며, 해당하는 그룹에 따라 색상 지정
for node2 in nodes:
    group = node2['data']['group']
    color = group_to_color.get(group, "gray")  # group_to_color에 정의된 그룹이 아닐 경우 기본 색상으로 "gray" 사용
    # 노드 데이터에 style 속성 추가 및 background-color 설정
    node2['classes'] = color


edges = [
    {'data': {'source': source, 'target': target, 'weight': score}}
    for source, target, score in zip(df_edge['source'], df_edge['target'], df_edge['KappaScore'])
]


elements = nodes + edges

app.layout = html.Div([
    html.H1('Cytoscape_network', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='dropdown-update-layout',
        value='cose',
        clearable=False,
        options=[
            {'label': name.capitalize(), 'value': name}
            for name in ['cose', 'random', 'grid', 'circle', 'concentric', 'breadthfirst']
        ],
        style={'width': '30%'}
    ),
    html.H2(id='cytoscape-mouseoverNodeData-output-term'),
    html.H4(id='cytoscape-mouseoverNodeData-output-gene'),
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        stylesheet=[
            {
                "selector": 'node',
                'style': {
                    'content': 'data(label)',
                    'opacity': 0.8,
                    'text-opacity': 1, # text 투명도 설정
                    'height': 10,
                    'width': 10,
                    'font-size': '5px'
                }
            }
        ] + [
                {
                    "selector": f".{color}",
                    'style': {'background-color': color}
                } for color in colors
            ],
        layout={'name': 'cose'},
        style={'height': '100vh',
               'width': '80%'},
    ),
    html.H4("Result table"),

    dash_table.DataTable(
        data=result.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in result.columns],
        style_table={'width': '90%'},
        style_cell={'textAlign': 'left', 'font_family': 'notosans', 'font-size': '13px'},
    ),
    dcc.Store(id='intermediated-value')
])


@app.callback(Output('cytoscape', 'layout'),
              Input('dropdown-update-layout', 'value'))
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }

@app.callback(Output('cytoscape-mouseoverNodeData-output-term', 'children'),
              Input('cytoscape', 'mouseoverNodeData'))
def displayTapNodeData(data):
    if data:
        return "GO term: " + str(data['label'])

@app.callback(Output('cytoscape-mouseoverNodeData-output-gene', 'children'),
              Input('cytoscape', 'mouseoverNodeData'))
def displayTapNodeData(data):
    if data:
        return "Associated gene: " + str(data['gene']) + ", Term p-value: " + str(data['size'])



if __name__ == "__main__":
	app.run_server(debug=True, use_reloader=False)