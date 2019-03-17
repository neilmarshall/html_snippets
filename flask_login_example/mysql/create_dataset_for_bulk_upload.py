#! venv/bin/python3.7

import csv
import sqlite3

def main():
    with sqlite3.connect('app/comic_book_characters.db') as connection:
        connection.execute('''CREATE TEMP VIEW IF NOT EXISTS combined AS SELECT * FROM DC UNION SELECT * FROM Marvel;''')
        data = connection.execute('''SELECT hero_name, ID, ALIGN, GSM, SEX, EYE, HAIR, ALIVE, APPEARANCES FROM COMBINED ORDER BY hero_name;''')
    with open('mysql/comic_book_characters.txt', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    main()
