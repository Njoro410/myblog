from app import create_app,db
from app.models import User,Posts,Comments,Categories,Role
from flask_script import Manager, Server
from  flask_migrate import Migrate, MigrateCommand

app = create_app('development')

manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command('server',Server)
manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app = app, User=User, Posts = Posts, Comments = Comments, Role = Role, Categories = Categories )

if __name__ == '__main__':
    manager.run()