from django.core.management.base import BaseCommand
import csv
import sqlite3


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()

        create_table = '''CREATE TABLE category(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        slug TEXT NOT NULL);
                        '''

        cursor.execute(create_table)
        file = open('static/data/category.csv')
        contents = csv.reader(file)
        insert_records = "INSERT INTO category (id, name, slug) VALUES(?, ?, ?)"
        cursor.executemany(insert_records, contents)
        select_all = "SELECT * FROM category"
        rows = cursor.execute(select_all).fetchall()

        for r in rows:
            print(r)

        connection.commit()
        connection.close()
