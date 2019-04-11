import psycopg2
from django.shortcuts import render

from articles.crawler_test import Crawler


def test(request, keyword):
    a = Crawler(keyword=keyword)
    a.crawl()
    return render(request, 'index.html')


# def test():
#     print(' start')
#     conn = psycopg2.connect(
#         host="project-brunch.cvoqbij1g79e.ap-northeast-2.rds.amazonaws.com",
#         database="ec2_deploy_rds",
#         user="doh",
#         password="ehghks0102",
#         port=5432
#     )
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM articles_article WHERE article_txid='Epw_1'")
#     a = cur.fetchall()
#     print(a)
#
#
# if __name__ == '__main__':
#     test()
