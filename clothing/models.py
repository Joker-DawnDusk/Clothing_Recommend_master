from django.db import models
from django.db.models import Avg
from django.core import validators
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Genre'

    def __str__(self):
        return f"<Genre:{self.name}>"


class Clothes(models.Model):
    # 服装名称
    name = models.CharField(max_length=256)
    # 服装唯一id
    unique_id = models.CharField(max_length=256)
    # 服装id
    clothes_id = models.IntegerField()
    # 服装详情网页
    clothes_url = models.CharField(max_length=256, blank=True)
    # 类型
    genre = models.ManyToManyField(Genre)
    # 店铺
    shop = models.CharField(max_length=256, blank=True)
    # 价格
    price = models.CharField(max_length=256)
    # 服装之间相似度
    clothes_similarity = models.ManyToManyField("self", through="Clothes_similarity", symmetrical=False)

    class Meta:
        db_table = 'Clothes'

    def __str__(self):
        return f"<Clothes:{self.name},{self.clothes_id}>"

    def get_score(self):
        # 定义一个获取平均分的方法，模板中直接调用即可
        # 格式 {'score__avg': 3.125}
        result_dct = self.clothes_rating_set.aggregate(Avg('score'))
        try:
            # 只保留一位小数
            result = round(result_dct['score__avg'], 1)
        except TypeError:
            return 0
        else:
            return result

    def get_user_score(self, user):
        return self.clothes_rating_set.filter(user=user).values('score')

    def get_score_int_range(self):
        return range(int(self.get_score()))

    def get_genre(self):
        genre_dct = self.genre.all().values('name')
        genre_lst = []
        for dct in genre_dct.values():
            genre_lst.append(dct['name'])
        return genre_lst

    def get_similarity(self,k=5):
        # 获取5件最相似的服装的id
        similarity_clothes = self.clothes_similarity.all()[:k]
        print(similarity_clothes)
        return similarity_clothes


class Clothes_similarity(models.Model):
    clothes_source = models.ForeignKey(Clothes, related_name='clothes_source', on_delete=models.CASCADE)
    clothes_target = models.ForeignKey(Clothes, related_name='clothes_target', on_delete=models.CASCADE)
    similarity = models.FloatField()
    class Meta:
        # 按照相似度降序排序
        ordering = ['-similarity']


class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    rating_clothes = models.ManyToManyField(Clothes, through="Clothes_rating")

    def __str__(self):
        return "<USER:( name: {:},password: {:},email: {:} )>".format(self.name, self.password, self.email)

    class Meta:
        db_table = 'User'

class Clothes_rating(models.Model):
    # 评分的用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    # 评分的服装
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, unique=False)
    # 分数
    score = models.FloatField()
    # 评论、可选
    comment = models.TextField(blank=True)

    class Meta:
        db_table = 'Clothes_rating'

class Clothes_hot(models.Model):
    '''存放最热门的100件服装'''
    #服装外键
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    #评分人数
    rating_number = models.IntegerField()

    class Meta:
        db_table = 'Clothes_hot'
        ordering = ['-rating_number']