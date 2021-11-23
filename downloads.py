import crawlers as c


def to_excel():
    return c.df.to_excel('104JOB.xlsx', engine='xlsxwriter')
