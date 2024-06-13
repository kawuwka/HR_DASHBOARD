import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
from pages import info, company, department

external_stylesheets = [dbc.themes.JOURNAL]
app = Dash(__name__, external_stylesheets=external_stylesheets,  use_pages=True)
app.config.suppress_callback_exceptions = True

# Задаем аргументы стиля для боковой панели. Мы используем position:fixed и фиксированную ширину
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '16rem',
    'padding': '2rem 1rem',
    'background-color': '#fda3a3', # Цвет фона боковой панели меняем на тот, который больше всего подходит
}

# Справа от боковой панели размешается основной дашборд. Добавим отступы
CONTENT_STYLE = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}

sidebar = html.Div(
    [
        html.H2('HR-аналитика', className='display-6', style={'color': 'white'}),
        html.Hr(),
        html.P(
            'Учебный проект студента БСБО-15-21 Шатилиной Е.А.', className='lead', style={'color': 'white'}
        ),
        dbc.Nav(
            [
                dbc.NavLink('Информация о проекте', href='/', active='exact', style={'color': 'white'}),
                dbc.NavLink('Общая статистика', href='/page-1', active='exact', style={'color': 'white'}),
                dbc.NavLink('Статистика по отделам', href='/page-2', active='exact', style={'color': 'white'}),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id='page-content', style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id='url'), sidebar, content])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname == '/':
        return info.layout
    elif pathname == '/page-1':
        return company.layout
    elif pathname == '/page-2':
        return department.layout
    return html.Div(
        [
            html.H1('404: Not found', className='text-danger'),
            html.Hr(),
            html.P(f'The pathname {pathname} was not recognised...'),
        ],
        className='p-3 bg-light rounded-3',
    )

if __name__ == '__main__':
    app.run_server(debug=True)