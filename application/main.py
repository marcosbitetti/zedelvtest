import os, sys
import connexion
from dotenv import (
    load_dotenv
)

import common.db as db
from controllers.home import router as home_router

path, fl = os.path.split(os.path.realpath(__file__))

print('Startuping server...')
load_dotenv()
print('listening on port %s' % os.getenv('port'))

if not db.initialize():
    sys.exit()
db.migrate()
print('Database connected')

def test_start():
    assert True

main_app = connexion.FlaskApp(os.getenv('app_name'), specification_dir='%s/api/' % path)
main_app.add_api('swagger.yml')
main_app.app.register_blueprint(home_router)


main_app.run(host='0.0.0.0', port=os.getenv('port'), debug=os.getenv('environment') != 'prod')

