import pymongo
from bson import ObjectId
from itertools import imap
from config import CONFIG
from pprint import pprint

database = CONFIG[u'db'][u'database']
collection = CONFIG[u'db'][u'collection']
connector = CONFIG[u'db'][u'client']
class Model(dict):
    """
    Wraps mongodb document
    """
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    def save(self, collection):
        print "allo: {}".format(self)
        bulk = self.db[collection].initialize_ordered_bulk_op()
        if not self._id:
            try:
                bulk.insert(self)
                result = bulk.execute()
                print("result: {}".format(result))
            except Exception as err:
                print "Error insertion {}".format(err)
            
        else:
            print ("update id: {}".format(self._id))
            self.db[collection].update(
                { "_id": ObjectId(self._id) }, self)

    def save_multiple(self, collection, docs):
        bulk = self.db[collection].initialize_ordered_bulk_op()
        if not self._id:
            try:
                for doc in docs:
                    bulk.insert(doc)
                    print("insert doc: {}".format(doc))
                result = bulk.execute()
                return result
            except Exception as err:
                print "Error insertion {}".format(err)

    def reload(self, collection):
        if self._id:
            self.update(self.db[collection]\
                    .find_one({"_id": ObjectId(self._id)}))

    def remove(self, collection):
        if self._id:
            self.db[collection].remove({"_id": ObjectId(self._id)})
            self.clear()


class Document(Model):
    client = pymongo.MongoClient(connector)
    db = client[database]
    