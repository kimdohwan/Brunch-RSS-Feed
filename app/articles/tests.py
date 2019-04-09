import psycopg2


def test():
    print(' start')
    conn = psycopg2.connect(
        host='project-brunch.cvoqbij1g79e.ap-northeast-2.rds.amazonaws.com',
        database='eb_docker_brunch_production',
        user='doh',
        password='ehghks0102',
        port='5432'
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM articles_article")
    a = cur.fetchall()
    print(a)

if __name__ == '__main__':
    test()