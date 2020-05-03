import os, json
import pymongo

# setup database
mdb = None

def initialize():
    global mdb
    try:
        mdb = pymongo.MongoClient(
            '%s:%s' % (os.getenv('db_host'), os.getenv('db_port')),
            username=os.getenv('db_user'),
            password=os.getenv('db_pwd'),
            authSource=os.getenv('db_databasename'),
            authMechanism='SCRAM-SHA-1'
        ).get_database(os.getenv('db_databasename'))
        return True
    except ImportError:
        print('Error connection to database')
    return False

def collection(name):
    return mdb.get_collection(name)

def create_collection(name):
    return mdb.create_collection(name)


def migrate():
    global mdb
    # drop existing collection
    collection('partners').drop()
    # recreate it
    partners = create_collection('partners')
    # unique indexes
    partners.create_index([('document', pymongo.ASCENDING)], unique=True)
    partners.create_index([('id', pymongo.ASCENDING)], unique=True)
    # populate
    path, fl = os.path.split(os.path.realpath(__file__))
    with open('%s/../test_data/pdvs.json' % path, 'r') as file:
        data = json.load(file)
    partners.insert_many(data['pdvs'])