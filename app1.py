from flask import Flask, redirect, request, render_template, url_for
import crawlers as s

app1 = Flask(__name__)


@app1.route("/")
def index():
    return redirect(url_for('submit'))


# @app1.route("/post_submit", methods=['GET', 'POST'])
# def submit():
#     if request.method == 'POST':
#         return 'keyword: ' + request.form.get('keyword') + ' pages: ' + request.form.get('pages')
#     return render_template('main.html')


@app1.route("/post_submit2", methods=['GET', 'POST'])
def submit():
    request_method = request.method
    if request_method == 'POST':
        key_word = request.form.get('keyword')
        pages = request.form.get('pages')
        spider = s.main(key_word, pages)
    return render_template('main.html', request_method=request_method)


if __name__ == '__main__':
    app1.run(debug=True, port=5000)
