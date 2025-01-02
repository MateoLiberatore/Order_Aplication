from models.models import Client, Product, db
from app import app
from sqlalchemy import cast, String

def search(cls, dic_params):#check
    #recives a class and a dic. with the params to search

    query = cls.query 

    type_filters = {
        int: lambda column, value: column == value,
        float: lambda column, value: column == value,
        str: lambda column, value: cast(column, String).like(f"%{value}%")
    }

    for column_name, search_value in dic_params.items():

        column = getattr(cls, column_name, None)  
        
        if column:

            filter_operation = type_filters.get(type(search_value))# select filter using the type value in column
            if filter_operation:
                query = query.filter(filter_operation(column, search_value))# filter the column with de value in the parameter dict 
                
    results = query.all() 

    detailed_results = [ 
        {key: value for key, value in dic.__dict__.items() 
         if key != '_sa_instance_state'}
            for dic in results]
    return detailed_results #tuple of dict with the matches

def get_all(cls):  # check
    models = cls.query.order_by(cls.id).all()
    detailed_models = [
        {key: getattr(model, key) for key in model.__table__.columns.keys()}
        for model in models
    ]
    return detailed_models

def add(cls, dict_params):#check
    try:

        record = cls()
        for key,value in dict_params.items():
            if not hasattr(cls, key):
                return {"error":f"EL modelo '{cls.__name__}'no tiene un campo llamado '{key}' "}

            column = getattr(cls, key)

            if isinstance(column.type, db.Column) and not isinstance(value, column.type.python_type):
                return {"error": f"el campo '{key}' debe ser del tipo {column.type.python_type.__name__}"}, 400

            setattr(record, key, value)

        db.session.add(record)
        db.session.commit()
        return record, 201
    
    except Exception as e:
        db.session.rollback()
        return {"error": f"Error al agreagr el registro: {str(e)}"}, 500
    

def modify(cls,id,update_dic):#chequear

    model = db.session.get(cls, id)
    if not model:
        return {"error": f"{cls.__tablename__} con ID {id} no encontrado"}, 404
    
    for key, value in update_dic.items():

        if key in cls.__table__.columns:
            column_type = cls.__table__.columns[key].type.python_type
            if not isinstance(value,column_type):
                return {
                    "error": f"El campo '{key}' debe ser del tipo {column_type.__name__}"
                }, 400 
            setattr(cls, key, value)

        else: 
            return {
                "error": f"El campo '{key}' no existe en el modelo '{cls.__name__}'"
            }, 400
    try:
        db.session.commit()
        return {"success": f"{cls.__tablename__} con ID {id} modificado correctamente."}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"No se pudo modificar el registro: {str(e)}"}, 500

    
def delete_client(cls, client_id):

    client = db.session.get(Client, client_id)
    if not client:
        return{"error": "Cliente inexistente"}, 404

    try:
        db.session.delete(client)   
        db.session.commit()
        return {"message": "Cliente borrado con exito"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error":f"No se pudo eliminar el cliente: {str(e)}"}, 500



with app.app_context():
    data = {
        "name": "Pelota",
        "tag": "Deportes",
        "price": "20.02",
        "description": "Pelota de soccer",
        "stock": "5"
    } 

    #add(Product, data )
    #delete_client(4)
    #id = 3
    #modify_client(id, updated_data)
    print(get_all(Product))
    #print(search(Client, updated_data))

    




