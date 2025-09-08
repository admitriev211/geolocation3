from flask import Flask
from flask import render_template
import xlrd

app = Flask(__name__)

@app.route('/')
def show_heatmap(map_type = 'placemark'):
    fields = {
        'lon': 'Долгота',
        'lat': 'Широта',
        'potencial': 'Потенциал',
        'address': 'address'
    }

    xl = xlrd.open_workbook('address.xls', on_demand=True)
    df1 = xl.sheet_by_name('Лист1')
    # ищем нужные столбцы
    cols_need = {}
    for k, v in fields.items():
        for i in range(0, df1.ncols):
            if df1.cell(0, i).value == v:
                cols_need[k] = i

    # идем по строкам для преобразования даты
    rows = []
    for i in range(1, df1.nrows):
        row = {}
        row['id'] = i
        for k, v in cols_need.items():
            try:
                if str(df1.cell(i, v).value).split('.')[1] == '0':
                    row[k] = int(df1.cell(i, v).value)
                else:
                    row[k] = df1.cell(i, v).value
            except:
                row[k] = df1.cell(i, v).value
        rows.append(row)

    potencial = sorted(rows, key=lambda x: x['potencial'], reverse=True)

    return render_template('heatmap.html', potencial=potencial[:2000], map_type=map_type, success=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
