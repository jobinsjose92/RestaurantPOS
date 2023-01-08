from pos import db
from datetime import datetime

class association(db.Model):
    ticket_id = db.Column(db.Integer(), db.ForeignKey("customerticket.id"),primary_key=True)
    item_id = db.Column(db.Integer(), db.ForeignKey("menu.id"),primary_key=True)

class Customerticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    arrival = db.Column(db.DateTime, nullable=False,)
    departed = db.Column(db.DateTime, nullable=False)
    table_id = db.Column(db.Integer)
    waiter_id = db.Column(db.Integer, db.ForeignKey('waiter.id'))
    waiter = db.relationship('Waiter', backref=db.backref('tickets', lazy='dynamic'))
    item  = db.relationship("Menu",secondary="association", backref="menu")
    
    def __init__(self, arrival, departed,table_id,waiter):
        self.arrival = arrival
        self.departed = departed
        self.table_id = table_id
        self.waiter = waiter
         
    def __repr__(self):
        return '<CustomerTicketId %d>' % self.id

class Waiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    tax_number = db.Column(db.String(100))
    #products = db.relationship('Product', backref=db.backref('category'))
    
    def __init__(self, first_name,last_name,tax_number):
        self.first_name = first_name
        self.last_name = last_name
        self.tax_number = tax_number
        
    def __repr__(self):
        return '<Waiter &d>' % self.id
    


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100))
    descr = db.Column(db.String(100))
    price = db.Column(db.Float)
    
    #products = db.relationship('Product', backref=db.backref('category'))
    
    def __init__(self, item_name,descr,price):
        self.item_name = item_name
        self.descr = descr
        self.price = price
        
    def __repr__(self):
        return '<MenuId &d>' % self.id