
import datetime
import mysql.connector
import logging
import json
from json import JSONEncoder
from collections import namedtuple


class DateTimeEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()


def main(tableName):
    mydb = mysql.connector.connect(host="localhost", port=3306, user="root", password="123456", database='dbtest')

    table = tableName
    today = datetime.date.today()
    selectQuery = 'SELECT id, FirstName, LastName, Address, City, BirthDate FROM {} WHERE BirthDate >= {}'.format(table, today)
    logging.info('Table selected: {} using date: {}, Query: {}'.format(table, today, selectQuery))
    cursor = mydb.cursor()
    cursor.execute(selectQuery)
    listData = cursor.fetchall()

    PersonTuple = namedtuple("Person", "id first_name last_name address city birth_date")
    personsListTuple = [PersonTuple(*p) for p in listData]

    for p in personsListTuple:
        personId = p.id
        selectOrdersQuery = 'SELECT id, PersonId FROM Orders WHERE PersonId = {}'.format(personId)
        cursor = mydb.cursor()
        cursor.execute(selectOrdersQuery)
        listOrderData = cursor.fetchall()

        Order = namedtuple("Order", "id person_id")
        orders = [Order(*o) for o in listOrderData]

        print(p)

        print(orders)

        PersonT = namedtuple("Person", "id first_name last_name address city birth_date orders")
        personWithOrder = [p.id, p.first_name, p.last_name, p.address, p.birth_date, orders]
        #personFinal = Person(p.id, p.first_name, p.last_name, p.address, p.birth_date, orders)

        print("Person final: ", personWithOrder)
        print(json.dumps(personWithOrder), indent=5, cls=DateTimeEncoder)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('Persons')
