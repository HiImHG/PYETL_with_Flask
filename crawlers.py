import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import random

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44"
tmp_url = "https://www.104.com.tw/jobs/search/"


def main(area, job_cat_no, remote, key_word, pages):
    if ' ' in key_word:
        key_word = key_word.replace(' ', '%20')
    elif '　' in key_word:
        key_word = key_word.replace('　', '%20')

    if remote == '1, 2':
        data_str = """ro: 0
        jobcat: {}
        kwop: 11
        keyword: {}
        expansionType: job, area
        area: {}
        order: 14
        asc: 0
        page: 1
        mode: s
        jobsource: 2018indexpoc
        langFlag: 0
        remoteWork: {}""".format(job_cat_no, key_word, area, remote)
    else:
        data_str = """ro: 0
        jobcat: {}
        kwop: 11
        keyword: {}
        expansionType: job, area
        area: {}
        order: 14
        asc: 0
        page: 1
        mode: s
        jobsource: 2018indexpoc
        langFlag: 0""".format(job_cat_no, key_word, area)

    data = {r.split(': ')[0]: r.split(': ')[1] for r in data_str.split('\n')}
    tmp_url_parameters = [str(k) + "=" + str(v) + "&" for k, v in data.items()]
    tmp_url_parameters_str = ''.join(map(str, tmp_url_parameters))
    url = tmp_url + "?" + tmp_url_parameters_str

    headers1 = {
        "User-Agent": user_agent,
    }

    ss = requests.session()
    two_d_rows = []

    for i in range(1, int(pages) + 1):
        time.sleep(random.randint(3, 10) / 10)
        res = ss.get(url, headers=headers1)
        soup = BeautifulSoup(res.text, 'html.parser')
        title_soup_list = soup.select('div[class="b-block__left"]')
        for title_soup in title_soup_list:
            try:
                if title_soup.find('svg')['class'][1] == 'b-icon--w18':
                    continue
                else:
                    article_url_tmp = title_soup.select('a')[0]['href']
                    article_url_real = "https:" + (article_url_tmp.split('?'))[0]
                    random_end_url = ("https:" + (article_url_tmp.split('?'))[0]).split('/')[4]
                    article_url_for_js = "https://www.104.com.tw/job/ajax/content/" + random_end_url
                    referer = 'https://www.104.com.tw/job/' + random_end_url
                    headers2 = {
                        "User-Agent": user_agent,
                        "Referer": referer
                    }
                    res_article = ss.get(article_url_for_js, headers=headers2)
                    json_data = json.loads(res_article.text)
                    job_name = json_data['data']['header']['jobName']
                    comp_name = json_data['data']['header']['custName']
                    job_address = json_data['data']['jobDetail']['addressRegion'] + json_data['data']['jobDetail'][
                        'addressDetail']
                    job_description = json_data['data']['jobDetail']['jobDescription']
                    other = json_data['data']['condition']['other']
                    salary = json_data['data']['jobDetail']['salary']
                    welfare = '\n'.join([i for i in json_data['data']['welfare']['legalTag']] +
                                        [i for i in json_data['data']['welfare']['tag']])

                    rows = [job_name, comp_name, job_address, salary, article_url_real, job_description,
                            other, welfare]
                    two_d_rows.append(rows)
            except IndexError:
                continue
            except TypeError:
                continue

        data['page'] = i + 1
        tmp_url_parameters = [str(k) + "=" + str(v) + "&" for k, v in data.items()]
        tmp_url_parameters_str = ''.join(map(str, tmp_url_parameters))
        url = tmp_url + "?" + tmp_url_parameters_str

    df = pd.DataFrame(two_d_rows,
                      columns=["Job Title", "Company", "Company Address", "Salary", "Job Url",
                               "Job Description", "Other Requirements", "welfare"])
    df['Job Title'] = '<a href="' + df['Job Url'] + '">' + df['Job Title'] + '</a>'
    df = df.drop(["Job Url"], axis=1)
    return df
