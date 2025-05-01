from flask import Flask, render_template, request, send_file
import pandas as pd
import random
#import pdfkit
import os

app = Flask(__name__, template_folder='template')

# wkhtmltopdfのパスを指定（Windowsなら↓）
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# エクセル読み込み
file_path = "英単語小テスト.xlsx"
df = pd.read_excel(file_path, sheet_name=0)

selected_words = []  # 選ばれた単語リストを保持する

@app.route('/', methods=['GET', 'POST'])
def index():
    global selected_words

    if request.method == 'POST':
        start_num = int(request.form['start_num'])
        end_num = int(request.form['end_num'])

        print(f"★受信した範囲: {start_num}〜{end_num}")

        subset = df[(df['番号'] >= start_num) & (df['番号'] <= end_num)]

        print(f"★フィルタ後の件数: {len(subset)}")

        selected = subset.sample(n=min(20, len(subset)))

        selected_words = []
        for _, row in selected.iterrows():
            selected_words.append({
                '単語': row['単語'],
                '意味': row['意味']
            })

        return render_template('result.html', words=selected_words)

    return '''
        <form method="POST" action="/">
            開始番号: <input type="number" name="start_num"><br>
            終了番号: <input type="number" name="end_num"><br>
            <input type="submit" value="送信">
        </form>
    '''

#@app.route('/download_pdf')
#def download_pdf():
    # 選ばれた単語リストをHTML化
    rendered = render_template('pdf_template.html', words=selected_words)

    # PDFファイルを一時作成
    pdf_file = '単語テスト.pdf'
    pdfkit.from_string(rendered, pdf_file, configuration=config)

    # できたPDFをダウンロード
    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


