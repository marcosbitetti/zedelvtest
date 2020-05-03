import os
from flask import (
    Blueprint,
    send_file
)

router = Blueprint('home', __name__)
current_path, fl = os.path.split(os.path.realpath(__file__))

@router.route('/')
@router.route('/<path:path>')
def home(path='index.html'):
    return send_file('%s/../static/%s' % (current_path, path))
