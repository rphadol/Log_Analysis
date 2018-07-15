#!/usr/bin/env python

import psycopg2


def main():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect(dbname="news")
    c = db.cursor()
    c.execute("""select articles.title , count(*) as views from articles, log
    where articles.slug = substring(log.path,10) group by
    articles.title order by views DESC Limit 3;""")
    result = c.fetchall()
    print("Most Popular top three articles")
    for title, num in result:
        print(" \"{}\" --- {} views".format(title, num))
    c.close()

    db = psycopg2.connect(dbname="news")
    c = db.cursor()
    c.execute("select authors.name, count(*) as views from articles inner "
              "join authors on articles.author = authors.id inner join log "
              "on log.path like concat('%', articles.slug, '%') where "
              "log.status like '%200%' group "
              "by authors.name order by views desc")
    result = c.fetchall()
    print("       ")
    print("       ")
    print("Who are the most popular article authors of all time?")
    for name, num in result:
        print(" {} --- {} views".format(name, num))
    c.close()

    db = psycopg2.connect(dbname="news")
    c = db.cursor()
    c.execute("""select time, percentagefailed
              from percent_ount
              where percentagefailed > 1""")
    result = c.fetchall()
    print("       ")
    print("       ")
    print('On which days did more than 1% of requests lead to errors?')
    for days, percentagefailed in result:
        print('{0:%B %d, %Y}'
              '--- {1:.2f} %errors'.format(days, percentagefailed))
    c.close()
    db.close()


if __name__ == "__main__":
    main()
