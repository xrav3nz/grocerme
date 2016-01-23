#!venv/bin/python
import os
from grocerme import create_app
from grocerme.extensions import db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.environ.get('FLASK_CONFIG'))
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()