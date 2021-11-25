from flask import Flask, redirect, request, render_template, url_for, send_from_directory, send_file
import crawlers as s
import os
from io import BytesIO

app1 = Flask(__name__)
# app1.config['UPLOAD_PATH'] = './data'


@app1.route("/")
def index():
    return redirect(url_for('submit'))


@app1.route("/post_submit2", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        return redirect(url_for('html_table', key_word=request.form.get('key_word'), pages=request.form.get('pages')))
    return render_template('main.html')


# @app1.route("/post_submit", methods=['GET', 'POST'])
# def submit():
#     if request.method == 'POST':
#         return 'keyword: ' + request.form.get('keyword') + ' pages: ' + request.form.get('pages')
#     return render_template('main.html')


@app1.route('/pandas/<key_word>_<pages>', methods=("POST", "GET"))
def html_table(key_word, pages):
    global df
    df = s.main(key_word, pages)
    return render_template('simple.html',  tables=[(df.to_html(classes='data', index=False)).replace("\\n", "<br>").replace("\\r", "")], titles=df.columns.values,
                           key_word=key_word, pages=pages)

# @app1.route('/pandas/<key_word>_<pages>', methods=("POST", "GET"))
# def html_table(key_word, pages):
#     global df
#     df = s.main(key_word, pages)
#     if request.method == 'POST':
#         filename = s.to_excel(df).read()
#         return send_from_directory(app1.config['UPLOAD_PATH'], filename=filename, as_attachment=True, key_word=key_word, pages=pages)
#     return render_template('simple.html',  tables=[(df.to_html(classes='data', index=False)).replace("\\n", "<br>").replace("\\r", "")], titles=df.columns.values,
#                            key_word=key_word, pages=pages)


# @app1.route('/download', methods=['GET', 'POST'])
# def download():
#     if not os.path.exists('./data'):
#         os.mkdir('./data')
#     path = s.to_excel(df)
#     return render_template('download.html', send_from_directory('./data', path=path, as_attachment=True))

@app1.route('/download', methods=("POST", "GET"))
def send_html():
    if request.method == 'POST':
        output = BytesIO()
        filename = s.to_excel(df)
        filename.save()
        output.seek(0)
    return send_from_directory(output, as_attachment=True)


if __name__ == '__main__':
    app1.run(debug=True, port=5000)
