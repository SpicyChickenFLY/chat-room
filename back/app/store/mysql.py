from sqlalchemy import create_engine
from sqlalchemy.orm import contains_alias, sessionmaker
# 数据库引擎和会话创建

SQL_HOST = 'localhost'          # 数据库地址
SQL_PORT = '3306'               # 数据库端口
SQL_USERNAME = 'chat'           # 数据库用户名
SQL_PASSWORD = 'chat'         # 数据库密码
SQL_DATABASE = 'chat'    # 数据库名称

conn_str = f'mysql+pymysql://{SQL_USERNAME}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}'
engine = create_engine(conn_str)
Session = sessionmaker(bind=engine)

sql_session = Session()
