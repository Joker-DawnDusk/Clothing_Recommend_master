import csv


# class Modify():
#     def __init__(self):
#         # csv路径
#         self.info_save_path = './info/info.csv'
#
#     def change(self):

# import csv
# with open("./info/info.csv", encoding='utf-8') as f:
#     reader = csv.reader(f)
#     write = csv.writer(f)
#     for row in reader:
#         print(row[0])

# with open("./info/text.csv", encoding="utf-8") as f2:
#     write = csv.writer(f2)
#     write.w
#     for cal in write:
#         print(cal[0])

import pandas as pd
import numpy as np
# csv_path = './info/text.csv'
# df = pd.read_csv(csv_path)
#
# df.columns = ['X1', 'X2', 'X3', 'X4']
# df.index = range(df.shape[0])
# df.info()
#
#
# df = pd.read_csv(csv_path)
# df['X3'] = [i+1 for i in range(df.shape[0])]
# df.to_csv(csv_path, sep=',', index=False, header=True)
# print(df)
#
# import csv
# with open("./info/text.csv", encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)

# csv_path = './info/info.csv'
# df = pd.read_csv(csv_path)
# df['id'] = [i+1 for i in range(df.shape[0])]
# df.to_csv(csv_path, sep=',', index=False, header=True)

# import pymysql
# # 连接 StudentTest数据库
# config = {'host': 'localhost',
# 'port': 3306,
# 'user': 'root',
# 'passwd': '123456',
# 'db' : 'clothing_recommend_db',
# }
# conn = pymysql.connect(**config)


# from sqlalchemy import create_engine
#
# engine = create_engine('mysql+pymysql://root@localhost/{}'.format(clothing_recommend_db), encoding='utf-8')
# df.to_sql(table_name,con=engine(db_name),if_exists='append',index=True)


# import pandas as pd
# import pymysql
#
#
# # 用pandas读取csv
# # data = pd.read_csv(file_name,engine='python',encoding='gbk')
# data = pd.read_csv('./info/info.csv', encoding='utf-8')
#
# # 数据库连接
# conn = pymysql.connect(
#     user="root",
#     port=3306,
#     passwd="123456",
#     db="clothing_recommend_db",
#     host="127.0.0.1",
#     charset='utf8'
# )
#
# # 使用cursor()方法获取操作游标
# cursor = conn.cursor()
#
# #id,unique_id,name,clothes_url,poster_url,genre,shop,price
# # 数据过滤，替换 nan 值为 None
# data = data.astype(object).where(pd.notnull(data), None)
#
# for id, unique_id, name, clothes_url, poster_url, genre, shop, price in zip(
#         data['id'], data['unique_id'], data['name'], data['clothes_url'], data['poster_url'],
#         data['genre'], data['shop'], data['price']):
#
#     #CREATE_DATE = format_date(CREATE_DATE)  # 这里由于对日期有特殊需求，自己处理了一下，代码就不贴了，如无需要可略过。
#
#     dataList = [id, unique_id, name, clothes_url, poster_url, genre, shop, price]
#     #print(dataList)
#     #print(dataList)  # 插入的值
#
#
#     insertsql = "INSERT INTO clothes(id,unique_id,name,clothes_url,poster_url,genre,shop,price) VALUES(%s,%char,%char,%char,%char,%char,%char,%s)"
#     cursor.execute(insertsql, dataList)
#     conn.commit()


# import pandas as pd
# from sqlalchemy import create_engine
# from datetime import datetime
# from sqlalchemy.types import NVARCHAR, Float, Integer
#
# # 连接设置 连接mysql 用户名ffzs 密码666 地址localhost：3306 database：stock
# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/clothing_recommend_db')
# # 建立连接
# con = engine.connect()
# df = pd.read_csv('./info/info.csv', encoding='utf-8')
#
# # pandas类型和sql类型转换
# def map_types(df):
#     dtypedict = {}
#     for i, j in zip(df.columns, df.dtypes):
#         if "object" in str(j):
#             dtypedict.update({i: NVARCHAR(length=255)})
#         # if "float" in str(j):
#         #     dtypedict.update({i: Float(precision=2, asdecimal=True)})
#         # if "int" in str(j):
#         #     dtypedict.update({i: Integer()})
#     return dtypedict
#
# dtypedict = map_types(df)
# # 通过dtype设置类型 为dict格式{“col_name”:type}
# df.to_sql(name='clothes', con=con, if_exists='replace', index=False, dtype=dtypedict)


# import csv
# with open("./info/info.csv", encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         #id,unique_id,name,clothes_url,poster_url,genre,shop,price
#         a = row[0]
#         b = row[1]
#         c = row[2]
#         d = row[3]
#         e = row[5]
#         f = row[6]
#         g = row[7]
#         a = 'INSERT INTO `clothes` VALUES (' + ''' + a + ', ' + b + ', ' + c + ', ' + d + ', ' + e + ', ' + f + ', ' + g + ',' + ')' + ';'
#         with open('./info/text.txt', 'w', encoding='utf-8') as fb:
#             fb.write(a)

#INSERT INTO `clothes` VALUES ('16791', '10045029971637', '班尼路2022春夏新款潮流抗菌polo衫男休闲简约百搭港风翻领短袖上衣00AM', 'https://item.jd.com/10045029971637.html', 'T恤', '班尼路官方旗舰店', '￥99.00');



# import pymysql
# import codecs
# import csv
# #
# conn = pymysql.Connect(
#     host = 'localhost',
#     port = 3306,
#     user = 'root',
#     password = '123456',
#     db = 'clothing_recommend_db',
#     charset = 'utf8')
#
# cursor = conn.cursor()
#
# sql2 = "INSERT INTO clothes values ('%s','%s','%s','%s','%s','%s','%s','%s')"
# file = open('./info/info.csv', 'r', encoding='utf-8')
# file.readline()
#
# for i in file.readlines():
#     data = i.strip().split(',')
#     cursor.execute(sql2 % data)

# conn = pymysql.connect(host="127.0.0.1",port=3306,
#                    user="root",password="123456",
#                    db="clothing_recommend_db",charset="utf8")
# with codecs.open(filename='./info/info_1.csv', mode='r', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     head = next(reader)
#     print(head)
#     cur = conn.cursor()
#     for item in reader:
#         # if item[1] is None or item[1] == '':  # item[1]作为唯一键，不能为null
#         #     continue
#         args = item
#         cur.execute(sql2, args)
# conn.commit()
# cur.close()
# conn.close()


import csv
import random
def clothes():
    with open('./info/info_1.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            id = str(row[0])
            #L.append(id)
            genre = str(row[5])
            #L.append(genre)
            L = [id, genre]
            with open('./info/clothes.csv', 'a+', encoding='utf-8',  newline='') as f2:
                write = csv.writer(f2)
                write.writerow(L)
            L = []

def clothes_2():
    with open('./info/info_1.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            id = str(row[0])
            unique_id = str(row[1])
            clothes_id = str(row[0])
            name = str(row[2])
            clothes_url = str(row[3])
            poster_url = str(row[4])
            genre = str(row[5])
            shop = str(row[6])
            price = str(row[7])
            L = [id, unique_id, clothes_id, name, clothes_url, poster_url, genre, shop, price]
            with open('./info/info_2.csv', 'a+', encoding='utf-8',  newline='') as f2:
                write = csv.writer(f2)
                write.writerow(L)


def rating():
    last = '1'
    L = []
    for i in range(1, 26401):
        L.append(str(i))
    with open('./info/ratings.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            UserId = str(row[0])
            ClothesId = str(row[1])
            rating = str(row[2])
            time = str(row[3])
            if UserId == 'userId':
                continue
            with open('./info/ratings_1.csv', 'a+', encoding='utf-8', newline='') as f2:
                write = csv.writer(f2)
                if UserId == last:
                    if ClothesId not in L:
                        ClothesId = random.choice(L)
                else:
                    L = []
                    for i in range(1, 26401):
                        L.append(str(i))
                    if ClothesId not in L:
                        ClothesId = random.choice(L)
                detail = [UserId, ClothesId, rating, time]
                L.remove(ClothesId)
                write.writerow(detail)
            last = UserId

def similarity():
    L = []
    for i in range(1, 26401):
        L.append(str(i))
    with open('./info/movie_similarity.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            clothesId1 = str(row[0])
            clothesId2 = str(row[1])
            similarity = str(row[2])
            if clothesId1 == 'movie_id1':
                continue
            if clothesId1 not in L:
                continue
            if clothesId2 not in L:
                continue
            with open('./info/clothes_similarity2.csv', 'a+', encoding='utf-8', newline='') as f2:
                write = csv.writer(f2)
                detail = [clothesId1, clothesId2, similarity]
                write.writerow(detail)

similarity()
