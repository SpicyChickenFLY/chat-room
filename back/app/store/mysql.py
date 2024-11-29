from flask_sqlalchemy import SQLAlchemy


# 数据库引擎和会话创建

SQL_HOST = "localhost"  # 数据库地址
SQL_PORT = "3306"  # 数据库端口
SQL_USERNAME = "chat"  # 数据库用户名
SQL_PASSWORD = "chat"  # 数据库密码
SQL_DATABASE = "chat"  # 数据库名称
CONN_STR = f"mysql+pymysql://{SQL_USERNAME}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}"

def get_mysql_uri():
    return CONN_STR
