import pandas as pd

def format_values(value):
    match value:
        case 'sales':
            return 'Отдел продаж'
        case 'technical':
            return 'Технический'
        case 'support':
            return 'Отдел поддержки'
        case 'IT':
            return 'IT'
        case 'product_mng':
            return 'Продуктовые менеджеры'
        case 'RandD':
            return 'R&D-менеджеры'
        case 'marketing':
            return 'Отдел маркетинга'
        case 'accounting':
            return 'Бухгалтерия'
        case 'management':
            return 'Отдел менеджмента'
        case 'hr':
            return 'HR'
        case _:
            return value

def format_string(string):
    match string:
        case 'low':
            return 'Маленькая'
        case 'medium':
            return 'Средняя'
        case 'high':
            return 'Высокая'
        case _:
            return string

def format_accident(value):
    match value:
        case 1:
            return 'Было'
        case 0:
            return 'Не было'
        case _:
            return value

df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQ08XW2wvmOWH0Ea0f-ty4sRWpGc8xXiaUcALtdi9_nlRWlQSWPsOqJMiSZoIVMgTiJLZFAiWE1-N_w/pub?output=csv")
df['department'] = df['department'].apply(format_values)
df['salary'] = df['salary'].apply(format_string)
df['work_accident'] = df['work_accident'].apply(format_accident)

all_depart = df['department'].unique()
