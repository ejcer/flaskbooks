import os
from app import create_app
from flask.ext.script import Manager, Shell

#TODO dont forget to go back and add/initialize your db dependencies/alchemy

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app) #TODO will need to update this with db and models

manager.add_command("shell", Shell(make_context=make_shell_context))



if __name__ == "__main__":
    manager.run()
