from models.models import db
from sqlalchemy import cast, String, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.attributes import InstrumentedAttribute
from flask import jsonify
from ast import literal_eval


def search(cls, dic_params): 
    '''
    cls parameter: class in models.py
    select filter depending on the dictionary content
    cleaning of the query removing instance of the ORM object
    '''
    try:     
        query = cls.query

        if 'id' in dic_params and isinstance(dic_params['id'], int):
            result = query.filter_by(id=dic_params['id']).first()
            return result, 200

        type_filters = {
            int: lambda column, value: column == value,
            float: lambda column, value: column == value,
            str: lambda column, value: cast(column, String).ilike(f"%{value}%")
        }

        filters = []

        for column_name, search_value in dic_params.items():
            column = getattr(cls, column_name, None)  
            if column:
                filter_operation = type_filters.get(type(search_value))
                if filter_operation:
                    filters.append(filter_operation(column, search_value))

        if filters:
            query = query.filter(or_(*filters))

        results = query.all() 
        return results, 200

    except (SyntaxError, ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        return {"error": f"Error al obtener todos: {str(e)}"}, 500

    

def get_all(cls):
    '''
    cls parameter: class in models.py
    all data in db regarding a determined class model
    '''
    try:
        models = cls.query.order_by(cls.id).all()
        return models
    
    except (SyntaxError, ValueError,SQLAlchemyError) as e:
        db.session.rollback()
        return {"error": f"Error al generar la busqueda: {str(e)}"}, 500 

def add(cls, dict_params):
    try:
        record = cls()

        for key, value in dict_params.items():
            if not hasattr(cls, key):
                return {"error": f"El modelo '{cls.__name__}' no tiene un campo '{key}'"}, 400

            column = getattr(cls, key)

            if isinstance(column, InstrumentedAttribute):
                try:
                    python_type = column.property.columns[0].type.python_type
                    
               
                    if value is None and column.nullable is False:
                        return {"error": f"El campo '{key}' no puede ser nulo."}, 400
                        
                    if isinstance(value, str) and value.strip() == "" and column.nullable is False:
                        return {"error": f"El campo '{key}' no puede estar vacío."}, 400

                    converted_value = python_type(value) if value is not None else None
                    
                    setattr(record, key, converted_value)
                except (AttributeError, ValueError, TypeError) as e:
                    return {"error": f"El campo '{key}' debe ser del tipo {python_type.__name__}. Error: {str(e)}"}, 400

        print(record)
        db.session.add(record)
        db.session.commit()
        return {"success": f"{cls.__name__} creado exitosamente"}, 201

    except Exception as e:
        db.session.rollback()
        print(repr(e))
        return {"error": f"Error al agregar el registro: {str(e)}"}, 500

    
def modify(cls,id,update_dic):  #check
    '''
    cls parameter: class in models.py
    check for class.item exists
    convert dict values to original data types
    check for field-key value maches
    commit.
    '''
    model = db.session.get(cls, id)
    print("model: ", model)
    if not model:
        return {"error": f"{cls.__tablename__} con ID {id} no encontrado"}, 404
    
    try:
        #print(update_dic)
        data = update_dic.copy() 
        print(data)
    except (SyntaxError, ValueError,SQLAlchemyError) as e:
        #logging de error
        return {"error": f"Error en la conversión de datos: {str(e)}"}, 400

    for key, value in data.items():

        if key in cls.__table__.columns:
            column_type = cls.__table__.columns[key].type.python_type

            if not isinstance(value, column_type):
                return {"error": f"El campo '{key}' debe ser del tipo {column_type.__name__}"}, 400
            
            setattr(model, key, value)
        else:
            return {"error": f"El campo '{key}' no existe en el modelo '{cls.__name__}'"}, 400

    try:
        #logging de el commit
        db.session.commit()
        return {"success": f"{cls.__tablename__} con ID {id} modificado correctamente."}, 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return {"error": f"No se pudo modificar el registro: {str(e)}"}, 500
    
def delete(cls,id): #check
    '''
    cls parameter: class in models.py
    query class.element[id]
    delete.
    '''
    print("Intentando borrar ID:", id)
    element = db.session.get(cls, id)
    print("Elemento encontrado:", element)
    
    if not element:
        return {"error": f"No se encontró el cliente con ID {id}"}, 404
    try:
        db.session.delete(element)   
        db.session.commit()
        return {"message": "Cliente borrado con éxito"}, 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return {"error":f"No se pudo eliminar el cliente: {str(e)}"}, 500
    
