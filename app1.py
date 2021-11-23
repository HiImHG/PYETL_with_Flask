from flask import Flask, redirect, request, render_template, url_for
import crawlers as s
import numpy as np
import pandas as pd

app1 = Flask(__name__)
# df = s.main('工程師', '1')


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
    df = s.main(key_word, pages)
    return render_template('simple.html',  tables=[df.to_html(classes='data', index=False)], titles=df.columns.values,
                           key_word=key_word, pages=pages)


if __name__ == '__main__':
    app1.run(debug=True, port=5000)
