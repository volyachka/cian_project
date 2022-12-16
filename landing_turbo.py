import json
import os
import re
from dash import Dash, dcc, html
from dash import callback_context
from dash import Input, Output, State, callback, MATCH, ALL
import plotly.express as px
import pandas as pd

from math import log

import data_process_for_visual
import mortgage_api
import information

import data_process_for_visual as dp

from types import SimpleNamespace



# Предобработка данных

df = pd.read_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8', index_col=0)

for col in df.columns:
    if 'Unnamed' in col:
        df.drop(labels=col, axis=1, inplace=True)

df = df.astype({'price_mortgage': int,
                'rooms_cnt': int,
                'lon': float,
                'lat': float,
                'dist_to_metro': float})

df['index'] = df.index
df['price_log'] = df['price_mortgage'].apply(lambda x: log(x))

# там есть квартира за 32 рубля...
# df = df[df['price_mortgage'] >= int(1e6)]

INITIAL_FEE_MIN = int(1e6)
INITIAL_FEE_MAX = int(11e6)
INITIAL_FEE_STEP = int(1e5)

METRO = list(map(lambda x: x.title(), information.metro_names))

MIN_PRICE = df[['price_mortgage']].values.min()
MAX_PRICE = df[['price_mortgage']].values.max()

# Отрисовка

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

mapbox_access_token = "pk.eyJ1IjoiZGFuLXZvbG9kaW4iLCJhIjoiY2xib2NkejRqMDdraDN1bGNsYjBxZjFiNiJ9.DH4q91ELiKdvwE2ghTCk3Q"
mapbox_style = "mapbox://styles/dan-volodin/clbod4hw2000g14qrh1bgp83d"


def map_from_df(data):
    px.set_mapbox_access_token(mapbox_access_token)
    fig_map = px.scatter_mapbox(data, lat="lat", lon="lon",
                                hover_name="title",
                                custom_data=["index"],
                                color="price_log", size="rooms_cnt",
                                size_max=10, zoom=12,
                                color_continuous_scale="dense",
                                mapbox_style='streets',
                                center=dict(lon=37.6225, lat=55.75))

    plot_layout = {
        "title": "Map",
        "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
        "font": {"size": 12, "color": "white"},
        "showlegend": False,
        "plot_bgcolor": "#141414",
        "paper_bgcolor": "#141414"
    }

    fig_map.update_layout(plot_layout)
    fig_map.update_coloraxes(showscale=False)

    return fig_map


app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)

app.title = "Mortgage"


GITHUB_LINK = os.environ.get(
    "GITHUB_LINK",
    "https://github.com/volyachka/cian_project",
)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Какую квартиру Вы ищите?", className="header"),
                        html.P(
                            "Удобное метро:", className="subheader",
                            id="metro-text"
                        ),
                        dcc.Dropdown(METRO, id='metro-dropdown', multi=True),
                        html.P(
                            "Стоимость квартиры:", className="subheader",
                            id="price-slider-text"
                        ),
                        html.P(
                            "От: ", className="subheader",
                            id="min-price-text"
                        ),
                        dcc.Input(type="number", placeholder="Минимальная цена...",
                                  id="min-price-input", step=None,
                                  min=MIN_PRICE, max=MAX_PRICE,
                                  value=MIN_PRICE,
                                  required=True
                                  ),
                        html.P(
                            "До: ", className="subheader",
                            id="max-price-text"
                        ),
                        dcc.Input(type="number", placeholder="Минимальная цена...",
                                  id="max-price-input", step=None,
                                  min=MIN_PRICE, max=MAX_PRICE,
                                  value=MAX_PRICE,
                                  required=True
                                  ),
                        html.H4("Какие условия ипотеки Вас интересуют?", className="header"),
                        html.P(
                            "Первоначальный взнос: ", className="subheader",
                            id="initial-fee-text"
                        ),
                        dcc.Input(type="number", placeholder="Первоначальный взнос...",
                                  id="initial-fee-input", step=None,
                                  min=INITIAL_FEE_MIN, max=INITIAL_FEE_MAX,
                                  value=INITIAL_FEE_MIN,
                                  required=True
                                  ),
                        dcc.Slider(min=INITIAL_FEE_MIN, max=INITIAL_FEE_MAX,
                                   step=INITIAL_FEE_STEP, value=INITIAL_FEE_MIN,
                                   id='initial-fee-slider',
                                   marks={INITIAL_FEE_MIN: "1 млн.",
                                          INITIAL_FEE_MAX: "11 млн."}
                                   )
                    ],
                    id="initial-fee",
                    className="colorscale pb-20",
                ),
                html.Div(
                    [
                        html.P("Срок выплаты ипотеки:", className="subheader",
                               id='mortgage-years-text'),
                        dcc.Slider(marks={1: '1',
                                          2: '2',
                                          3: '4',
                                          4: '5',
                                          5: '10',
                                          6: '15',
                                          7: '20',
                                          8: '25',
                                          9: '30'},
                                   value=1,
                                   step=None,
                                   id='mortgage-years-slider'
                                   )
                    ],
                    className="pb-20",
                ),
                html.Div(
                    [
                        dcc.Checklist(options=[{'label': 'У меня есть ребенок, родившийся после 2018', 'value': '1'}],
                                      id='mortgage-children-2018',
                                      labelClassName="label__option",
                                      inputClassName="input__option"
                                      )
                    ],
                    className="pb-20",
                ),
            ],
            className="three columns app__left__section"
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H1("DVD-ипотека")
                                    ],
                                    className="header__title",
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            "Нажмите на интересующую вас квартиру или выберите при помощи лассо"
                                        )
                                    ],
                                    className="header__info pb-20",
                                )
                            ],
                            className="header pb-20",
                        ),
                        html.Div(
                            [
                                dcc.Loading(
                                    [
                                        dcc.Graph(
                                            id="map",
                                            figure=map_from_df(df),
                                            clickData={'points': [{'customdata': ["Nothing"]}]}
                                        )
                                    ],
                                    id="graph-loader"
                                )
                            ],
                            className="graph__container",
                        ),
                    ],
                    className="container",
                )
            ],
            className="five columns app__central__section",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Span("Предложения ипотеки", className="subheader"),
                        html.Span("  |  "),
                        html.Span(
                            "Настройте желаемые условия выше и выберите квартиру", className="small-text"
                        ),
                        dcc.Loading(
                            html.P(id="mortgage-list", className="info__container", children="Сначала выберите квартиру"),
                            type="dot",
                        ),
                    ],
                    className="pb-20 content-block",
                ),
                html.Div(
                    [
                        html.Span("Выбранные квартиры", className="subheader"),
                        html.Span("  |  "),
                        html.Span(
                            "Нажмите на квартиру на карте или выберите с помощью лассо",
                            className="small-text",
                        ),
                        dcc.Loading(
                            html.P(id="selected-flats", className="info__container scroll__section", children="Ничего не выбрано"),
                            type="dot"
                        )
                    ],
                    className="pb-20",
                    id="flats-selector"
                )
                # html.Div(
                #     [
                #         html.P(
                #             [
                #                 "Dash/Python code on ",
                #                 html.A(
                #                     children="GitHub.",
                #                     target="_blank",
                #                     href=GITHUB_LINK,
                #                     className="red-ish",
                #                 ),
                #             ]
                #         ),
                #         html.P(
                #             [
                #                 "DVD Production",
                #             ]
                #         ),
                #     ],
                #     id="contacts"
                # ),
            ],
            className="one-third column app__right__section",
        ),
        dcc.Store(id="annotation_storage")
    ]
)


def create_flat_div(flat_ind):
    flat_ind = int(flat_ind)
    flat = df[df["index"] == flat_ind]

    div = html.Div(className="flat-box",
                   children=[
                       html.Div(className="image-container", children=[
                           html.Img(className="flat-image", src=img_url) for img_url in json.loads(flat['photos'].values[0].replace('\'', '\"'))
                       ]),
                       html.Ul(className="flat-box-list", children=[
                           html.Li(className="flat-price", children=flat['price_spaces'] + '\u20bd'),
                           html.Li(className="flat-title", children=flat['title']),
                           html.Li(className="flat-floor", children="Этаж: " + flat['floor']),
                           html.Li(className="flat-address", children=flat['address_line']),
                           html.A(className="button", href=flat['flat_url'].values[0], target="_blank", children="Подробнее"),
                           html.Button(className="button", n_clicks=0,
                                       id={'type': 'show-mortgage',
                                           'index': flat_ind
                                       },
                                       value="Рассчитать ипотеку"),
                       ]),
                       html.Hr()
                   ])
    return div


cached_flats = SimpleNamespace(
    selected_data=None,
    clicked_data=None
)
@callback(
    Output('selected-flats', 'children'),
    Input('map', 'selectedData'),
    Input('map', 'clickData')
)
def update_flats_list(selectedData, clickData):
    if selectedData is not None and selectedData != cached_flats.selected_data:
        list = [create_flat_div(point['customdata'][0]) for point in selectedData["points"]]
    elif clickData["points"][0]["customdata"][0] == "Nothing":
        return "Ничего не выбрано"
    else:
        list = [create_flat_div(point['customdata'][0]) for point in clickData["points"]]

    cached_flats.selected_data = selectedData
    cached_flats.click_data = clickData

    return html.Div(children=list, id='selected-flats-list')


def create_mortgage_div(mortgage):
    # div = html.Div(className="flat-box",
    #                children=[
    #                    html.Div(className="image-container", children=[
    #                        html.Img(className="flat-image", src=img_url) for img_url in json.loads(flat['photos'].values[0].replace('\'', '\"'))
    #                    ]),
    #                    html.Ul(className="flat-box-list", children=[
    #                        html.Li(className="flat-price", children=flat['price_spaces'] + '\u20bd'),
    #                        html.Li(className="flat-title", children=flat['title']),
    #                        html.Li(className="flat-floor", children="Этаж: " + flat['floor']),
    #                        html.Li(className="flat-address", children=flat['address_line']),
    #                        html.A(className="button", href=flat['flat_url'].values[0], target="_blank", children="Купить")
    #                    ])
    #                ])
    return "Сначала выберите квартиру"


cached_mortgage = SimpleNamespace(
    flat_ind=0,
    div="Сначала выберите квартиру, лол"
)

@callback(
    Output('mortgage-list', 'children'),
    Input('mortgage-years-slider', 'value'),
    Input('initial-fee-input', 'value'),
    Input('mortgage-children-2018', 'value'),
    Input({'type': 'show-mortgage', 'index': ALL}, 'n_clicks'),
    State({'type': 'show-mortgage', 'index': ALL}, 'id'),
)
def update_mortgage_list(years, initial_fee, children_2018, n_clicks, button_id):
    if len(n_clicks) == 0 or len(n_clicks) == n_clicks.count(0):
        return "Сначала выберите квартиру"
    callback_trigger = callback_context.triggered_prop_ids
    if "show-mortgage" not in list(callback_trigger.keys())[0]:
        flat_ind = cached_mortgage.flat_ind
    else:
        flat_ind = list(callback_context.triggered_prop_ids.values())[0]["index"]
    price = df[df['index'] == flat_ind]["price_mortgage"].values[0]

    if children_2018 is None or len(children_2018) == 0:
        children_2018 = 0
    else:
        children_2018 = 1

    mortgages = mortgage_api.get_mortgage(initialFee=initial_fee,
                                          price=price,
                                          isHaveChildBefore2018=children_2018,
                                          period=years
                                          )

    block = html.A(className="button", href=mortgages, target="_blank", children="Предложения ипотек для Вас"),
    # return create_mortgage_div(mortgages[0])
    cached_mortgage.flat_ind = flat_ind
    cached_mortgage.div = block
    return block


@app.callback(
    Output('initial-fee-input', 'value'),
    Input('initial-fee-slider', 'value'))
def update_initial_fee_input(value):
    return value


@app.callback(
    Output('initial-fee-text', 'children'),
    Input('initial-fee-input', 'value'))
def update_initial_fee_text(value):
    if value is None:
        return "Первоначальный взнос:"
    value_spaces = data_process_for_visual.num_to_str(value)
    return f"Первоначальный взнос: {value_spaces} руб."


@app.callback(
    Output('mortgage-years-text', 'children'),
    Input('mortgage-years-slider', 'value'))
def update_mortgage_years_text(value):
    values = ['1 год', '2 года', '4 года', '5 лет', '10 лет', '15 лет', '20 лет', '25 лет', '30 лет']
    if value is None:
        return "Срок выплаты ипотеки:"
    return "Срок выплаты ипотеки: " + values[value - 1]


@app.callback(
    Output('min-price-text', 'children'),
    Input('min-price-input', 'value'))
def update_min_price_text(value):
    if value is None:
        return "От: "
    value_spaces = data_process_for_visual.num_to_str(value)
    return f"От: {value_spaces} руб."


@app.callback(
    Output('max-price-text', 'children'),
    Input('max-price-input', 'value'))
def update_min_price_text(value):
    if value is None:
        return "До: "
    value_spaces = data_process_for_visual.num_to_str(value)
    return f"До: {value_spaces} руб."


@app.callback(
    Output('map', 'figure'),
    Input('min-price-input', 'value'),
    Input('max-price-input', 'value'),
    Input('metro-dropdown', 'value')
)
def update_map(min_price, max_price, metro):
    df_filtered = df[(df['price_mortgage'] >= min_price) & (df['price_mortgage'] <= max_price)]
    return map_from_df(df_filtered)


if __name__ == "__main__":
    app.run_server(debug=True)