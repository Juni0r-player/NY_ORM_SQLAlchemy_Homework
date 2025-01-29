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
    
    books = relationship('Book', back_populates='publisher')


class Book(Base):
    __tablename__ = 'book'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    id_publisher = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('publisher.id'), nullable=False)
    
    def __str__(self):
        return f'{self.title}'
    
    publisher = relationship(Publisher, back_populates='books') # связь с таблицей
    stock_book = relationship('Stock', back_populates='book_publisher')
    
    
class Shop(Base):
    __tablename__ = 'shop'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False) 

    def __str__(self):
        return f'{self.name}'
    
    stock_shop = relationship('Stock', back_populates='shop_publisher')
    
    
class Stock(Base):
    __tablename__ = 'stock'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_book = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('book.id'), nullable=False)
    id_shop = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('shop.id'), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer)          

    book_publisher = relationship(Book, back_populates='stock_book')
    shop_publisher = relationship(Shop, back_populates='stock_shop')
    stock_sale = relationship('Sale', back_populates='stock')
    
    
class Sale(Base):
    __tablename__ = 'sale'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)   
    date_sale = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    id_stock = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('stock.id'), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    
    def __str__(self):
        return f'{self.price} | {self.date_sale}'
    
    stock = relationship(Stock, back_populates='stock_sale')
        
def create_tables(engine):
    Base.metadata.drop_all(engine) # удалить все таблицы
    Base.metadata.create_all(engine) # create_all - параметр создания таблиц.

session.close_all()    



    
    

 
    