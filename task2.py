from sqlite3 import connect
import requests

DOMAIN = "https://recruitment.developers.emako.pl/products/example?id="

sql = connect(database="database.sqlite")
cursor = sql.cursor()

def fetch_api(index):
    endpoint = DOMAIN + index
    return requests.get(endpoint).json()

def type_check(data):
    if data['type'] == 'product':
        insert_product(data)
    elif data['type'] == 'bundle':
        insert_bundle(data)

def insert_product(response_API):
    if response_API['type'] == 'product':
            for item in response_API["details"]["supply"]:
                for stock in item["stock_data"]:
                    cursor.execute(
                        "INSERT INTO product_stocks (time, product_id, variant_id, stock_id, supply) VALUES ('%s','%s','%s','%s','%s')"
                        %
                        (response_API['created_at'], response_API['id'], item["variant_id"], stock['stock_id'], stock['quantity']))
    sql.commit()

def insert_bundle(response_API):
    for index in range(len(response_API['bundle_items'])):
        single_response = fetch_api(str(response_API['bundle_items'][index]['id']))
        for _ in range(response_API['bundle_items'][index]['quantity']):
            insert_product(single_response)

def main():
    index = input('Wpisz id produktu: ')
    response_api = fetch_api(str(index))
    type_check(response_api)

main()

sql.close()