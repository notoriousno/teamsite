from jinja2 import Environment, FileSystemLoader, select_autoescape
from twisted.enterprise.adbapi import ConnectionPool

from routes.root import Root


def main():
    # SQLite "connection"
    db_pool = ConnectionPool('sqlite3', 'sportsteam.sqlite', check_same_thread=False)

    # web template engine
    jinja_env = Environment(
        loader = FileSystemLoader('./templates'),
        autoescape = select_autoescape(['html'])
    )

    app = Root(jinja_env, db_pool)
    app.router.run('0.0.0.0', 8888)


main()  
