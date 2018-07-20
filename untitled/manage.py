from flask_script import Manager
from untitled import app
from flask_migrate import  MigrateCommand,Migrate
from db import db
from model import User
##init创建迁移仓库
##migrate迁移脚本
##upgrade更新数据库
manager=Manager(app)
Migrate=Migrate(app,db)
manager.add_command("db",MigrateCommand)

if __name__ == '__main__':

    manager.run()
