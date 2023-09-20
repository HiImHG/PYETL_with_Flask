from flask import Flask, redirect, request, render_template, url_for, make_response
import crawlers as s
import job_category as cat
from pandas import ExcelWriter
import io
import time
import requests
import logging
import xlsxwriter

app = Flask(__name__)

session = requests.session()

job_cat_1 = cat.create_cat(session)
area_cat = cat.create_area_show_dict(cat.area_json(session), 'des')
area_raw = cat.area_json(session)


@app.route("/")
def index():
    return redirect(url_for('submit'))


@app.errorhandler(404)
def page_not_found(e):
    logging.warning('User raised an 404: {error}'.format(error=str(e)))
    return render_template('404.html')


@app.route('/post_submit', methods=['GET', 'POST'])
def submit():
    image_path = '/static/images/github.png'
    link_url = 'https://github.com/HiImHG/PYETL_with_Flask'
    if request.method == 'POST':
        area_list = ','.join(cat.area_no_list(area_raw, request.form.getlist('selected_items')))
        area_name_list = ', '.join(request.form.getlist('selected_items'))
        remote_list = request.form.get('remote_only')
        return redirect(url_for('html_table',
                                area_no='6001000000' if area_list == '' else area_list,
                                area_name='台灣地區' if area_name_list == '' else area_name_list,
                                job_cat=request.form.get('job_item'),
                                job_cat_no=job_cat_1[request.form.get('job_item')],
                                remote_work='null' if remote_list != '1, 2' else remote_list,
                                key_word=request.form.get('key_word'),
                                pages=request.form.get('pages'))
                        )
    return render_template('main.html', items=job_cat_1, areas=area_cat, image_path=image_path, link_url=link_url)


@app.route('/pandas/<area_no>_<area_name>_<job_cat>_<job_cat_no>_<remote_work>_<key_word>_<pages>',
           methods=['POST', 'GET'])
def html_table(area_no, area_name, job_cat, job_cat_no, remote_work, key_word, pages):
    global df
    df = s.main(area_no, job_cat_no, remote_work, key_word, pages)
    return render_template('result.html', tables=[
        (df.to_html(classes='data', index=False, escape=False)).replace("\\n", "<br>").replace("\\r", "").replace("\\t",
                                                                                                                  " ")],
                           titles=df.columns.values, area_no=area_no, area_name=area_name, job_cat=job_cat,
                           job_cat_no=job_cat_no, remote_work=remote_work, key_word=key_word, pages=pages)


@app.route('/exportUser')
def export_user():
    out = io.BytesIO()
    writer = ExcelWriter(out, engine='xlsxwriter')
    try:
        new_df = cat.df_remake(df)
        new_df.to_excel(writer, index=False)
        writer.close()
        out.seek(0)
        resp = make_response(out.getvalue())
        cur_time = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        resp.headers['Content-Disposition'] = 'attachement; filename=104JOB_{}.xlsx'.format(cur_time)
        resp.headers['Content-Type'] = 'application/ms-excel; charset=utf-8'

        return resp
    except NameError:
        return '請回上一頁重新點選下載'


if __name__ == '__main__':
    app.run()
