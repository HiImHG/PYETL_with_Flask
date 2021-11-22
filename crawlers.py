import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44"
tmp_url = "https://www.104.com.tw/jobs/search/"


def main(key_word, pages):
    if ' ' in key_word:
        key_word = key_word.replace(' ', '%20')

    data_str = """ro: 0
    kwop: 11
    keyword: {}
    expansionType: job
    order: 14
    asc: 0
    page: 1
    mode: s
    jobsource: 2018indexpoc
    langFlag: 0""".format(key_word)

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
        res = ss.get(url, headers=headers1)
        soup = BeautifulSoup(res.text, 'html.parser')
        titleSoupList = soup.select('div[class="b-block__left"]')
        for title_soup in titleSoupList:
            try:
                title = title_soup.select('a')[0].text
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
                jobName = json_data['data']['header']['jobName']
                jobDescription = json_data['data']['jobDetail']['jobDescription']
                other = json_data['data']['condition']['other']
                jobCategory = [i['description'] for i in json_data['data']['jobDetail']['jobCategory']]

                Python_related = ['Python', 'python', 'PYTHON']
                AI_related = ['人工智慧', '機器學習', '深度學習', 'AI', 'Machine Learning']
                SQL_related = ['SQL', 'MYSQL', 'mysql', 'MySQL', 'NoSQL']
                Python_Tools = ['Pytorch', 'Tensorflow', 'Keras']

                Python_true = 0
                AI_true = 0
                sql_true = 0
                tools_true = 0
                for Py_related in Python_related:
                    if Py_related in jobName:
                        Python_true += 1
                    elif Py_related in jobDescription:
                        Python_true += 1
                    elif Py_related in other:
                        Python_true += 1
                    else:
                        pass
                if Python_true > 0:
                    Python = "O"
                else:
                    Python = "X"

                for ai_re in AI_related:
                    if ai_re in jobName or ai_re in jobDescription or ai_re in other:
                        AI_true += 1
                    else:
                        pass
                if AI_true > 0:
                    AI = "O"
                else:
                    AI = "X"

                for sql in SQL_related:
                    if sql in jobName or sql in jobDescription or sql in other:
                        sql_true += 1
                    else:
                        pass
                if sql_true > 0:
                    SQL = "O"
                else:
                    SQL = "X"

                for ptool in Python_Tools:
                    if ptool in jobName or sql in jobDescription or sql in other:
                        tools_true += 1
                    else:
                        pass
                if tools_true > 0:
                    pytools = "O"
                else:
                    pytools = "X"

                rows = [jobName, article_url_real, jobCategory, jobDescription, other, Python, AI, SQL, pytools]
                two_d_rows.append(rows)
            except IndexError as e:
                pass

        data['page'] = i + 1
        # print(data['page'])
        tmp_url_parameters = [str(k) + "=" + str(v) + "&" for k, v in data.items()]
        tmp_url_parameters_str = ''.join(map(str, tmp_url_parameters))
        url = tmp_url + "?" + tmp_url_parameters_str
        # print(url)

    df = pd.DataFrame(two_d_rows,
                      columns=["Job Title", "Job Url", "Job Category", "Job Description", "Other Requirements",
                               "Python", "AI(機器學習)", "SQL相關", "Python 相關套件工具"])
    # df.to_excel('104JOB.xlsx', engine='xlsxwriter')


if __name__ == "__main__":
    main()