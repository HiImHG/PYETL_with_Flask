from flask import Flask, redirect, request, render_template, url_for, make_response
import crawlers as s
from pandas import ExcelWriter
import io
import time
import os

app1 = Flask(__name__)


@app1.route("/")
def index():
    return redirect(url_for('submit'))


@app1.route("/post_submit2", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        return redirect(url_for('html_table', key_word=request.form.get('key_word'), pages=request.form.get('pages')))
    return render_template('main.html')


@app1.route('/pandas/<key_word>_<pages>', methods=("POST", "GET"))
def html_table(key_word, pages):
    global df
    df = s.main(key_word, pages)
    return render_template('result.html', tables=[
        (df.to_html(classes='data', index=False)).replace("\\n", "<br>").replace("\\r", "").replace("\\t", " ")],
                           titles=df.columns.values, key_word=key_word, pages=pages)


@app1.route('/exportUser')
def export_user():
    out = io.BytesIO()
    writer = ExcelWriter(out, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()
    out.seek(0)
    resp = make_response(out.getvalue())
    cur_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    resp.headers['Content-Disposition'] = 'attachement; filename=104JOB_{}.xlsx'.format(cur_time)
    resp.headers['Content-Type'] = 'application/ms-excel; charset=utf-8'

    return resp


if __name__ == '__main__':
    app1.run()
