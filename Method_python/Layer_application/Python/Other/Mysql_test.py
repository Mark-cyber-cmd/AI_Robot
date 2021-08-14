import mysql.connector

mady = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd=r"dingyiming1203"  # 数据库密码
)

print(mady)
