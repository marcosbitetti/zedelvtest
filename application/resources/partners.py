from math import cos, sin, sqrt, atan2, radians, pi
from numpy import arange
from pymongo import errors as errors
import common.db as db

#
# Module Partners
#

COLLECTION = 'partners'

# approximation reference https://www.usna.edu/Users/oceano/pguth/md_help/html/approx_equivalents.htm
def approximate_km2degree(km):
    return (km * 0.01) / 1.11


# https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0
    dlat = radians(lat2) - radians(lat1)
    dlon = radians(lon2) - radians(lon1)
    a = sin(dlat / 2.0) ** 2.0 + cos(lat1) * cos(lat2) * sin(dlon / 2.0) ** 2.0
    c = 2.0 * atan2(sqrt(a), sqrt(1.0 - a))
    return R * c


def create(partner):
    #print(partner)
    collection = db.collection(COLLECTION)
    # not a good way, but simple to improve faster
    partner['id'] = collection.estimated_document_count() + 1

    try:
        result = collection.insert_one(partner)
        if not result.inserted_id:
            return {'status': 'error', 'message': 'Can\'t add documet' }
    except errors.DuplicateKeyError:
        return {'status': 'error', 'message': 'Duplicate field "document"'}
    except:
        return {'status': 'error', 'message': 'Can\'t add documet'}

    return {'status': 'ok', 'insertedId': partner['id']}


def get(id):
    data = db.collection(COLLECTION).find_one({'id': '%i' % id}, {'_id': 0})
    return data

def list():
    return []

def search(lat, lon, radius):
    rad_angle = approximate_km2degree(radius)

    # draw a circular poligon to use in search
    poligon = []
    for a in arange(-pi, pi - (pi/4.0), pi/4.0):
       poligon.append([lat + rad_angle*cos(a), lon + rad_angle*sin(a)])
    poligon.append(poligon[0]) # close poligon

    geo_query = {'coverageArea': {'$geoIntersects': {'$geometry': {'type': "Polygon", 'coordinates': [poligon]}}}}

    data = []
    for i in db.collection(COLLECTION).find(geo_query, {'_id': 0, 'document': 0, 'coverageArea': 0}):
        coord = i['address']['coordinates']
        i['storeDist'] = distance(lat, lon, coord[0], coord[1])
        data.append(i)

    # sort result for nearest partner
    data = sorted(data, key = lambda k: k['storeDist'])

    return data

