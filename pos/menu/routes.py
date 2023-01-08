from flask import request, jsonify, Blueprint
from pos import db
from pos.menu.models import Customerticket,Menu,Waiter
from datetime import datetime
import json

menu = Blueprint('menu', __name__)

@menu.route('/')
@menu.route('/home')
def home():
    return "Welcome to the Catalog Home."

@menu.route('/customerTicket/<id>')
def ticket(id):
    ticket = Customerticket.query.get_or_404(id)
    return 'Tableid - %s, Waiterid- %s' % (ticket.table_id, ticket.waiter_id)

@menu.route('/customertickets')
def tickets():
    tickets = Customerticket.query.all()
    res = {}
    for ticket in tickets:
        res[ticket.id] = {
            'arrival': ticket.arrival,
            'departure': ticket.departed,
            'waiter': ticket.waiter.first_name
        }
    return jsonify(res)


@menu.route('/waiters')
def waiters():
    waiters = Waiter.query.all()
    res = {}
    for waiter in waiters:
        res[waiter.id] = {
            'Firstname': waiter.first_name,
            'Lastname': waiter.last_name,
            'Taxno': waiter.tax_number
        }
    return jsonify(res)

@menu.route('/menuitems')
def menuitems():
    items = Menu.query.all()
    res = {}
    for item in items:
        res[item.id] = {
            'Itemname': item.item_name,
            'Description': item.descr,
            'Price': item.price
        }
    return jsonify(res)

@menu.route('/createTicket', methods=['POST',])
def creat_Ticket():
    arrival = request.json.get('arrival')
    arr = datetime.strptime(arrival, '%d/%m/%Y %H:%M:%S')
    departed = request.json.get('departed')
    dep = datetime.strptime(departed, '%d/%m/%Y %H:%M:%S')
    table_id = request.json.get('tableid')
    waiter_name = request.json.get('waitername')
    waitername= Waiter.query.filter_by(first_name=waiter_name).first()
    
    newTicket = Customerticket(arr,dep,table_id, waitername)
    db.session.add(newTicket)
    db.session.commit()
    return 'New Ticket created.'

@menu.route('/Hire-Waiter', methods=['POST', ])
def create_waiter():
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    taxno = request.json.get('taxno')
    waiter = Waiter(firstname,lastname,taxno)
    db.session.add(waiter)
    db.session.commit()
    return 'Category created'


@menu.route('/AddMenu', methods=['POST', ])
def create_menu():
    itemname = request.json.get('itemname')
    descr = request.json.get('descr')
    price = request.json.get('price')
    menu = Menu(itemname,descr,price)
    db.session.add(menu)
    db.session.commit()
    return 'New Item created'

@menu.route('/AddItemsticket', methods=['POST', ])
def add_item_ticket():
    itemname = request.json.get('itemname')
    ticketid = request.json.get('ticketid')
    items = Menu.query.filter_by(item_name=itemname).first()
    ticket = Customerticket.query.filter_by(id=ticketid).first()
    ticket.item.append(items)
    
    db.session.commit()
    return 'New Item added'

@menu.route('/customerTicketitems/<ticketid>')
def ticketitems(ticketid):
    items = Customerticket.query.filter_by(id=ticketid).first()
    res={}
    for item in items.item:
        res[item.id]={'items':item.item_name,'price':item.price}
     
    
    return jsonify(res)


@menu.route('/customerTicketcost/<ticketid>')
def ticketcost(ticketid):
    items = Customerticket.query.filter_by(id=ticketid).first()
    sum=0
    for item in items.item:
        sum+=item.price
     
    
    return 'cost=$%f'%(sum)


@menu.route('/totalrevenue')
def total():
    items = Customerticket.query.all()
    
    itemC=0
    for ticket in items:
      sum=0
      for item in ticket.item:
          sum+=item.price
          
      itemC+=sum
        
    
    
    return 'Total Revenue=$%f'%(itemC)

'''
    
@menu.route('/createTickets', methods=['POST',])
def create_products():
    import json
    data = json.loads(request.data)
    for product in data:
     arrival = request.json.get('arrival')
     departed = request.json.get('departed')
     table_id = request.json.get('table_id')
     waitername = request.json.get('waitername')
     waiter= Waiter.query.filter_by(firstname=waitername).first()
     
     newTicket = CustomerTicket(arrival, departed,table_id, waiter)
     db.session.add(newTicket)
     db.session.commit()
     
    return 'tickets created.'
    '''