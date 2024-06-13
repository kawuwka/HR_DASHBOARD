from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df, all_depart

layout = dbc.Container([
    dbc.Row ([
        dbc.Col(
                html.Div([
                html.H3('Подробная информация о выбранном отделе'),
                html.Hr(style={'color': 'black'}),
            ], style={'textAlign': 'center'})
        )
    ]),

    html.Br(),

    dbc.Row ([
        dbc.Col([
            html.P('Выберите отдел:')
        ],width=2),
        dbc.Col([
            dcc.Dropdown(
                id = 'crossfilter-depart',
                options = [{'label': i, 'value': i} for i in all_depart],
                value = all_depart[0],
                multi = False
            )
        ],width=3)]),

    html.Br(),
    dbc.Container([
    dbc.Row ([
        dbc.Col([
            dbc.Card([
                    dbc.CardHeader('Нынешнее число сотрудников в отделе'),
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src='/static/images/employee.png')], width= 4),
                    dbc.Col([
                        dbc.CardBody(
                            html.P(
                            id='card_text1',
                            className='card-value'),
                            )], width= 8),
                    ])
                ], color = 'success', outline=True, style={'textAlign': 'center', 'height': '100%'}),
            ], width=3),
        dbc.Col([
            dbc.Card([
                    dbc.CardHeader('Средняя удовлетворенность сотрудников в отделе'),
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src='/static/images/satisfaction.png')], width= 4),
                    dbc.Col([
                        dbc.CardBody(
                            html.P(
                            id='card_text2',
                            className='card-value'),
                        )], width= 8),
                    ])
                ], color = 'success', outline=True, style={'textAlign': 'center', 'height': '100%'}),
            ], width=3),

        dbc.Col([
            dbc.Card([
                    dbc.CardHeader('Процент повышения сотрудников в отделе'),
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src='/static/images/promotion.png')], width= 4),
                    dbc.Col([
                        dbc.CardBody(
                            html.P(
                            id='card_text3',
                            className='card-value'),
                            )], width= 8),
                    ])
                ], color = 'success', outline=True, style={'textAlign': 'center', 'height': '100%'}),
            ], width=3),

        dbc.Col([
            dbc.Card([
                    dbc.CardHeader('Среднее количество часов, отработанных в месяц'),
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src='/static/images/montly_hours.png')], width= 4),
                     dbc.Col([
                        dbc.CardBody(
                            html.P(
                            id='card_text4',
                            className='card-value'),
                            )], width= 8),
                    ])
                ], color = 'success', outline=True, style={'textAlign': 'center', 'height': '100%'}),
            ], width=3)
    ]) ]), 
    html.Br(),
    dbc.Container([
        dbc.Row ([
            dbc.Col([
                html.Div(dcc.Graph(id='pie'),
                style={'width': '80%', 'float': 'left', 'display': 'inline-block'})
                ]),
            dbc.Col([
                html.Div(dcc.Graph(id='histogram'),
                style={'width': '100%', 'float': 'right', 'display': 'inline-block'})
                ]),

        ])
    ]),             
    dbc.Container([
        dbc.Row ([
            dbc.Col([
                html.Div(dcc.Graph(id='scatter'),
                style={'width': '100%', 'float': 'right', 'display': 'inline-block'}),
            ])
        ])
    ])
])

@callback(
    [Output('card_text1','children'),
    Output('card_text2','children'),
    Output('card_text3','children'),
    Output('card_text4','children'),
    ],
    [Input('crossfilter-depart', 'value'),
    ]
)

def update_card(depart):
    df_depart=df[(df['department'] == depart) & (df['left'] == 0)]

    ct1=str(df_depart['left'].count())
    ct2=str(round(df_depart['satisfaction_level'].mean(), 2)) 
    ct3=str(round(((sum(df_depart['promotion_last_5years'] == 1))*100)/df_depart['promotion_last_5years'].count(), 2)) + ' ' + '%'
    ct4=str(round(df_depart['average_montly_hours'].mean(), 2)) + ' ' + 'часов'
       
    return ct1, ct2, ct3, ct4

@callback(
    Output('scatter', 'figure'),
    [Input('crossfilter-depart', 'value')]
)
def update_scatter(depart):
    df_depart=df[(df['department'] == depart) & (df['left'] == 0)]
    figure = px.scatter(
        df_depart,
        x = 'average_montly_hours',
        y = 'satisfaction_level',
        size = 'last_evaluation',
        color='last_evaluation',
        labels={'last_evaluation': 'Последняя оценка сотрудника', 'average_montly_hours': 'Среднее количество часов в месяц', 'satisfaction_level': 'Удовлетворенность сотрудника'}
    )

    figure.update_layout(
        title='Зависимость удовлетворенности сотрудника от среднего количества часов в месяц по последней оценке сотрудника',
        title_x=0.5
    )

    return figure

@callback(
    Output('histogram', 'figure'),
    [Input('crossfilter-depart', 'value')]
)
def update_histogram(depart):
    df_depart=df[(df['department'] == depart) & (df['left'] == 0)]
    figure = px.histogram(
        df_depart,
        x = 'number_project',
        color='number_project',
        color_discrete_sequence= px.colors.sequential.Plasma_r,
        labels={'count': 'Количество сотрудников','number_project': 'Количество проектов'}
    )

    figure.update_layout(
        title='Распределение числа проектов',
        title_x=0.5,
        yaxis_title_text='Количество сотрудников', 
        legend=dict(visible=False)
    )

    return figure


@callback(
    Output('pie', 'figure'),
    [Input('crossfilter-depart', 'value')],
)
def update_pie(depart):
    df_depart=df[(df['department'] == depart) & (df['left'] == 0)]
                
    df_counts = df_depart['work_accident'].groupby(df_depart['work_accident']).count().reset_index(name='Количество сотрудников')
        
    figure = px.pie(
        df_counts,
        values='Количество сотрудников',
        names=df_counts['work_accident'],
        color_discrete_sequence= px.colors.sequential.Plasma_r,
        labels={'work_accident': 'Несчастные случаи'}

    )
    
    figure.update_layout(
        title='Несчастные случаи',
        title_x=0.5,
    )
    return figure