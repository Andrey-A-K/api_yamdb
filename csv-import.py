import argparse
import csv
import sqlite3


def copy_csv_to_db(path_to_csv, table_name):
    with open(path_to_csv) as file:
        line = 0
        for row in csv.reader(file):
            line += 1
            if line == 1:
                values = '?'
                headers = (', '.join(row))
                for value in range(1, len(row)):
                    values += ', ?'
            insert_records = (
                'INSERT INTO {table} ({headers}) VALUES ({values})'
            ).format(table=table_name, headers=headers, values=values)
            if line != 1:
                try:
                    cursor.execute(insert_records, row)
                except sqlite3.IntegrityError as err1:
                    msg1 = (
                        '\033[1;31m' + 'Похоже с данными что-то не так '
                        'или таблица уже заполнена.' + '\033[0m' + '\nОшибка:'
                    )
                    print(msg1, err1)
                    return False
                except sqlite3.OperationalError as err2:
                    msg2 = (
                        '\033[1;31m' + 'Похоже на то, что что-то '
                        'не так с названиями или количеством столбцов '
                        'в CSV или DB.' + '\033[0m' + '\nОшибка:'
                    )
                    print(msg2, err2)
                    return False
    return True


def check_result(path_to_db, table_name, result=None):
    select_all = 'SELECT * FROM {table}'.format(table=args.table)
    db_echo = cursor.execute(select_all).fetchall()
    if result and db_echo:
        print(
            'В таблицу {table} базы данных {db} записаны '
            'следующие строки:'.format(
                table=table_name,
                db=path_to_db
            )
        )
        for line in cursor.execute(select_all).fetchall():
            print('\033[32m' + 'Записана строка: ' + '\033[0m', line)
        print('\n Итого в базу записано {qty} строк'.format(qty=len(db_echo)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', help='Path to database')
    parser.add_argument('--csv', help='Path to csv file')
    parser.add_argument('--table', help='SQL Table name')
    args = parser.parse_args()

    connection = sqlite3.connect(args.db)
    cursor = connection.cursor()

    result = copy_csv_to_db(path_to_csv=args.csv, table_name=args.table)
    check_result(path_to_db=args.db, table_name=args.table, result=result)

    connection.commit()
    connection.close()
