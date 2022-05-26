# 基于协同过滤的服装推荐系统

------

**设计参考：**[https://github.com/hhmy27/Movies_Recommend]()

**数据来源：**用户评分数据来自于**MovieLens**的ml-latest-small数据集，累计10w+评分数据；服装信息按照提前设定的服装类型`/clothing/static/clothes/info/genre.txt`分别爬取得到，相关程序是`util/JDClothing.py`

**本系统运行方法：**

本项目所需数据库为`database/clothing_recommend_db.sql`，直接导入即可

在`Clothing_Recommend_master/Clothing_Recommend_system/settings.py`中设置好自己的数据库参数

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'clothing_recommend_db',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
```

此处以本人设置为例

使用PyCharm启动项目(其他软件没用过)，打开Terminal运行`python manage.py runserver`，在`127.0.0.1:8000`即可看到系统运行界面

后台地址：`127.0.0.1:8000/admin`，需要先在Terminal运行`python create superuser`创建管理员(用户名和密码)