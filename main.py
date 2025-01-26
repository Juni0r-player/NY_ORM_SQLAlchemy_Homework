import sqlalchemy
from sqlalchemy.orm import sessionmaker # для подключения к бд
from sqlalchemy.orm import declarative_base, relationship
import os
import dotenv

dotenv.load_dotenv()
DSN = os.getenv('DSN')

engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher' # аттрибут - название таблицы
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(40), unique=True, nullable=False)
    
    def __str__(self):
        return f'{self.id}:{self.name}'

class Book(Base):
    __tablename__ = 'book'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    id_publisher = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('publisher.id'), nullable=False)
    
    publisher = relationship(Publisher, backref='publisher') # связь с таблицей

class Shop(Base):
    __tablename__ = 'shop'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False) 

class Stock(Base):
    __tablename__ = 'stock'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_book = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('book.id'), nullable=False)
    id_shop = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('shop.id'), nullable=False)          

    book_publisher = relationship(Publisher, backref='book')
    shop_publisher = relationship(Publisher, backref='shop')
    
class Sale(Base):
    __tablename__ = 'sale'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)   
    date_sale = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    id_stock = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('stock.id'), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    
    publisher = relationship(Publisher, backref='stock')
        
def create_tables(engine):
    Base.metadata.drop_all(engine) # удалить все таблицы
    Base.metadata.create_all(engine) # create_all - параметр создания таблиц.


if __name__ == '__main__':
    create_tables(engine) # создаем таблицы
    

 
    