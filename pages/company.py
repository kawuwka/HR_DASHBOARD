from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df, all_depart

layout = dbc.Container([
    dbc.Row ([
        dbc.Col( html.Div([
                html.H1("Общая статистика по компании"),
                html.P("Анализ основных показателей по сотрудникам в компании"),
                html.Hr(style={'color': 'black'}),
            ], style={'textAlign': 'center'})
        )
    ]),

    html.Br(),
    dbc.Col([
            dcc.Dropdown(
                id = 'dummy',
                options = [{'label': i, 'value': i} for i in all_depart],
                value = None,
                multi = False,
                style={'display': 'none'}
            )
        ],width=3),

    html.Br(),

    dbc.Container([
        dbc.Row ([
            dbc.Col([
                dbc.Card([
                        dbc.CardHeader('Общее число сотрудников'),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/images/employee.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(
                                html.P(
                                id='card_text5',
                                className='card-value'),
                                )], width= 8),
                        ])
                ], color = 'success', outline=True, style={'textAlign': 'left'}),
                ], width=3),
            dbc.Col([
                    html.Img(src='/static/images/company.jpg', width = 830),
                            ])
                ]),
    dbc.Row ([
            dbc.Col([
                html.Div(dcc.Graph(id='pie1'),
                style={'width': '85%', 'float': 'left', 'display': 'inline-block'})
                ]),
            dbc.Col([
                html.Div(dcc.Graph(id='histogram1'),
                style={'width': '100%', 'float': 'right', 'display': 'inline-block'})
                ]),
        ])
    ]),

    dbc.Container([
        dbc.Row ([
            dbc.Col([
                html.Div(dcc.Graph(id='histogram2'),
                style={'width': '100%', 'float': 'center', 'display': 'inline-block'}),
            ])
        ])
    ])
])

@callback(
    Output('card_text5','children'),
    [Input('dummy', 'value')],
)

def update_card(dummy):
    df_depart=df[(df['left'] == 0)]
    ct5 = str(df_depart['left'].count())
    return ct5

@callback(
    Output('pie1', 'figure'),
    [Input('dummy', 'value')],
)

def update_pie(dummy): 
    df_depart=df[(df['left'] == 0)]
               
    df_counts = df_depart['department'].groupby(df['department']).count().reset_index(name='Количество сотрудников')

    figure = px.pie(
        df_counts,
        values='Количество сотрудников',
        names=df_counts['department'],
        color_discrete_sequence= px.colors.sequential.Plasma_r,
        labels={'department': 'Отдел'}
    )
    
    figure.update_layout(
        title='Доля работников в отделах',
        title_x=0.5,
        legend_title_text='Отдел',
    )

    return figure

@callback(
    Output('histogram1', 'figure'),
    [Input('dummy', 'value')]
)
def update_histogram(dummy):
    df_depart=df[(df['left'] == 0)]  

    figure = px.histogram(
        df_depart,
        x = 'department',
        color='salary',
        color_discrete_sequence= px.colors.sequential.Plasma_r,
        labels={'department': 'Отдел', 'salary': 'Зарплата'},
        barmode='group'
    )    
    
    figure.update_layout(
        title='Распределение зарплаты по отделам',
        title_x=0.5,
        legend_title_text='Зарплата',
        yaxis_title_text='Количество сотрудников'
        )
    return figure

@callback(
    Output('histogram2', 'figure'),
    [Input('dummy', 'value')]
)
def update_histogram(dummy):
    figure = px.histogram(
        df,
        x = 'time_spend_company',
        color='time_spend_company',
        color_discrete_sequence= px.colors.sequential.Plasma_r,
        labels={'department': 'Отдел', 'time_spend_company': 'Продолжительность работы в компании', 'count': 'Количество сотрудников, ушедших из компании'},
    )    
    
    figure.update_layout(
        title='Распределение ухода из компании исходя из проработанных лет',
        title_x=0.5,
        yaxis_title_text='Количество сотрудников',
        legend=dict(visible=False)
    )
    return figure
