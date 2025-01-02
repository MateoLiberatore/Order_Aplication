from src.models.models import Order, Client
from datetime import datetime


@classmethod
#all
def show_all_orders():
    #get all orders
    return Order.query.all()

@classmethod
#buscar ordenes por fecha
def show_date_orders(date):

    #truncar fecha a formato datetime
    date_obj = datetime.strptime(date, "%d-%m-%Y")
    formated_date = date_obj.strftime("%Y-%m-%d")

    start = datetime.combine(formated_date, datetime.min.time())
    end = datetime.combine(formated_date,datetime.max.time())

    orders = Order.query(Order).filter(Order.date_crerated >= start, Order.date_crerated <= end)
    return orders


@classmethod

def show_client_orders(client_name):

    clients = Client.query.filter(Client.name == client_name).all()

    if clients:
       
       result = []

    for client in clients:
           
            client_data = {
            'client_name': client.name,
            'client_id': client.id,
            'orders': []
            }

    for order in Order.query.filter(Order.client_id==client_data['client_id']).all():

            client_data['orders'].append(order)

    result.append(client_data)

    return result

#buscar ordenes por cliente
#buscar ordenes por id
#buscar ordenes donde aparezca un producto
#buscar ordenes por tag de producto
#modificar orden
#eliminar orden
#crear orden