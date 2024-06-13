import pandas as pd

def format_values(value):
        if value == 'sales':
            return 'Отдел продаж'
        elif value == 'technical':
            return 'Технический'
        elif value == 'support':
            return 'Отдел поддержки'
        elif value == 'IT':
            return 'IT'
        elif value == 'product_mng':
            return 'Продуктовые менеджеры'
        elif value == 'RandD':
            return 'R&D-менеджеры'
        elif value == 'marketing':
            return 'Отдел маркетинга'
        elif value == 'accounting':
            return 'Бухгалтерия'
        elif value == 'management':
            return 'Отдел менеджмента'
        elif value == 'hr':
            return 'HR'
        else:
            return value

def format_string(string):
        if string == 'low':
            return 'Маленькая'
        elif string == 'medium':
            return 'Средняя'
        elif string == 'high':
            return 'Высокая'
        else:
            return string
        
def format_accident(value):
        if value == 1:
            return 'Было'
        elif value == 0:
            return 'Не было'
        else:
            return value

df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQ08XW2wvmOWH0Ea0f-ty4sRWpGc8xXiaUcALtdi9_nlRWlQSWPsOqJMiSZoIVMgTiJLZFAiWE1-N_w/pub?output=csv")
df['department'] = df['department'].apply(format_values)
df['salary'] = df['salary'].apply(format_string)
df['work_accident'] = df['work_accident'].apply(format_accident)

all_depart = df['department'].unique()
