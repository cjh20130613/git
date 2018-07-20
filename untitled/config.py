import os
db="mysql"
dbconntector="pymysql"
dbuser="cjh"
dbpassword="cjh"
dbip="127.0.0.1"
dbport="3306"
dbname="ota"
dbcharset="utf8"
SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}".format(db,dbconntector,dbuser,dbpassword,dbip,dbport,dbname)
SQLALCHEMY_TRACK_MODIFICATIONS=False

SECRET_KEY=os.urandom(24)