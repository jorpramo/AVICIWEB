__author__ = 'jpradas'
import pymongo

MONGO_DATABASE = 'avici'
MONGODB_COLLECTION = 'servicios'
MONGODB_UNIQ_KEY = 'url'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True
MONGODB_URI = 'mongodb://avicibatch:avici2015@dbh63.mongolab.com:27637/avici'

class servicios:
    def LeeServicios(self, nombre='', actual=False):
        client = pymongo.MongoClient(MONGODB_URI)
        db = client.avici
        servicio=db.servicios
        if nombre=='':
            items=servicio.find({})
        else:
            items=servicio.find({"nombre":nombre})
        return items

    def LeeDatos(self, nombre=''):
        client = pymongo.MongoClient(MONGODB_URI)
        db = client.avici
        datos=db.datos_actual
        if nombre=='':
            items=datos.find({})
        else:
            items=datos.find({"nombre":nombre})
        return items


