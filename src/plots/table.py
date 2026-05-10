from dash import dash_table


def generar_table(df):
    table = dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl')
    return table