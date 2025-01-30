import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale
from add_data import add_data
import os
import dotenv

dotenv.load_dotenv()

DSN = os.getenv('DSN')

engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine) # создание таблиц
add_data() # добавление данных.


def get_shops(text):
    result = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        join(Publisher).\
        join(Stock).\
        join(Shop).\
        join(Sale)
    
    if text.isdigit():
        result = result.filter(Publisher.id == text).all()
    else:
        result = result.filter(Publisher.name == text).all()

    for i in result:
        print(f'{i[0]} | {i[1]} | {i[2]} | {i[3]}')

session.close()   
 

if __name__ == '__main__':
    text = input()
    get_shops(text)


