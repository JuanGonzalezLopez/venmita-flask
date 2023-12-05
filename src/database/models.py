from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    firstName = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)
    city = Column(String)
    country = Column(String)
    telephone = Column(String)

    # Relationships using ORM 2.0 style
    sent_transfers = relationship('Transfer', foreign_keys='Transfer.sender_id', back_populates='sender')
    received_transfers = relationship('Transfer', foreign_keys='Transfer.recipient_id', back_populates='receiver')
    transactions = relationship('Transaction',foreign_keys='Transaction.buyer_id' ,back_populates='buyer')


class Transfer(Base):
    __tablename__ = 'transfers'

    id = Column(Integer, primary_key=True,autoincrement=True)
    sender_id = Column(Integer, ForeignKey('people.id'))
    recipient_id = Column(Integer, ForeignKey('people.id'))
    amount = Column(Numeric(10, 2))
    date = Column(Date)

    # Relationships using ORM 2.0 style
    sender = relationship('Person', foreign_keys=[sender_id], back_populates='sent_transfers')
    receiver = relationship('Person', foreign_keys=[recipient_id], back_populates='received_transfers')


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True,autoincrement=True)
    buyer_id = Column(Integer, ForeignKey('people.id'))  # Referencing the Person's ID
    item = Column(String)
    price = Column(Numeric(10, 2))
    store = Column(String)
    transaction_date = Column(Date)

    # Update the relationship
    buyer = relationship('Person', back_populates='transactions')
    def __repr__(self):
        return (f" --------------------------- \n id = {self.id} \t\t| type = {type(self.id)}\n buyer_id = {self.buyer_id} \t\t| type = {type(self.buyer_id)}\n item = {self.item} \t\t| type = {type(self.item)} \n price = {self.price} \t\t| type = {type(self.price)} \n store = {self.store} \t\t| type = {type(self.store)} \n transaction_date = {self.transaction_date} \t\t| type = {type(self.transaction_date)} ")




class Promotion(Base):

    __tablename__ = 'promotions'



    id = Column(Integer, primary_key=True,autoincrement=True)
    client_email = Column(String)
    telephone = Column(String)
    promotion = Column(String)
    responded = Column(Boolean)
    person_id = Column(Integer, ForeignKey('people.id'), default=None, nullable=True)  # Linking to the Person's ID



    def __repr__(self):
        return (f" --------------------------- \n id = {self.id} \t\t| type = {type(self.id)}\n client_email = {self.client_email} \t\t| type = {type(self.client_email)}\n telephone = {self.telephone} \t\t| type = {type(self.telephone)} \n responded = {self.responded} \t\t| type = {type(self.responded)} \n person_id = {self.person_id} \t\t| type = {type(self.person_id)}")


