import json
from itertools import chain
import requests
import pandas as pd
import re

session = requests.session()


def create_cat(ss):
    url = 'https://static.104.com.tw/category-tool/json/JobCat.json'
    res = ss.get(url)
    _json = json.loads(res.text)

    job_cat_1_des = [i['des'] for i in _json]
    job_cat_1_no = [i['no'] for i in _json]
    job_cat_1 = {job_cat_1_des[i]: job_cat_1_no[i] for i in range(len(job_cat_1_des))}
    return job_cat_1


def area_json(ss):
    url = 'https://static.104.com.tw/category-tool/json/Area.json'
    res = ss.get(url)
    taiwan_list = json.loads(res.text)[0]
    return taiwan_list


def get_val(search_dict, key):
    new_list = []
    for elem in search_dict:
        if elem == key:
            new_list.append(search_dict[elem])
        if isinstance(search_dict[elem], list):
            for city in search_dict[elem]:
                retval = get_val(city, key)
                if retval is not None:
                    new_list.append(retval)
    return new_list


def create_area_show_dict(search_dict, key):
    area_raw = get_val(search_dict, key)[1:]
    new_dict = {area_raw[i][0]: list(chain.from_iterable(area_raw[i][1:])) for i in range(len(area_raw))}
    area = {'台灣地區': new_dict}
    return area


def area_no_list(show_dict, checkbox_item):
    no_list = []
    for item in checkbox_item:
        if item not in show_dict.values():
            for city in show_dict['n']:
                if item not in city.values():
                    for county in city['n']:
                        if item in county.values():
                            no_list.append(county['no'])
                        else:
                            continue
                else:
                    no_list.append(city['no'])
        else:
            no_list.append(show_dict['no'])
    return no_list


def df_remake(dataframe):
    dataframe['Job Link'] = dataframe['Job Title'].apply(lambda x: re.sub(r'<a href=\"([^\"]+)\">[^<]+</a>', r'\1', x))
    dataframe['Job Title'] = dataframe['Job Title'].apply(lambda x: re.sub(r'<a[^>]*>(.*?)</a>', r'\1', x))
    df_new = dataframe[['Job Title', 'Job Link', 'Company', 'Company Address', 'Salary', 'Job Description',
                        'Other Requirements', 'welfare']]
    return df_new