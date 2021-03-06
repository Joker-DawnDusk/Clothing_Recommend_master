import csv
import time
import os.path
from math import sqrt
from django.contrib import messages
from django.db.models import Avg, Count, Max
from django.http import HttpResponse, request
from django.shortcuts import render, redirect, reverse
from clothing.forms import RegisterForm, LoginForm, CommentForm
from django.views.generic import View, ListView, DetailView
from clothing.models import User, Clothes, Genre, Clothes_rating, Clothes_similarity, Clothes_hot

# DO NOT MAKE ANY CHANGES
BASE = os.path.dirname(os.path.abspath(__file__))

#--------------导入csv文件--------------#
# '''
# 导入服装类型
# '''
# def get_genre():
#     '''导入所有服装类型'''
#     path = os.path.join(BASE, 'static\clothes\info\genre.txt')
#     with open(path, encoding='utf-8') as fb:
#         for line in fb:
#             Genre.objects.create(name=line.strip())
#
#
# '''
# 导入服装信息
# '''
# def get_clothes_info():
#     '''导入所有服装信息，设置它们的类型'''
#     path = os.path.join(BASE, 'static\clothes\info\info.csv')
#     with open(path, encoding='utf-8') as fb:
#         reader = csv.reader(fb)
#         title = reader.__next__()
#         # 读取title信息  id,unique_id,name,clothes_url,poster_url,genre,shop,price
#         # 此处的unique_id代表服装唯一id，根据它来访问static文件夹下面的poster
#         title_dct = dict(zip(title, range(len(title))))
#         # print(title_dct)
#         for i,line in enumerate(reader):
#             m = Clothes.objects.create(name=line[title_dct['name']],
#                                        unique_id=line[title_dct['unique_id']],
#                                        clothes_url=line[title_dct['clothes_url']],
#                                        clothes_id=line[title_dct['clothes_id']],
#                                        shop=line[title_dct['shop']],
#                                        price=line[title_dct['price']])
#             # 先保存再建立关系
#             m.save()
#             # 建立类型关系
#             for genre in line[title_dct['genre']].split('|'):
#                 # 找到类型  genre_object
#                 go = Genre.objects.filter(name=genre).first()
#                 # print(go)
#                 m.genre.add(go)
#             if i % 10000 == 0:
#                 print(i)       # 控制台查看进度
#
#
# '''
# 导入用户信息
# '''
# def get_user_and_rating():
#     '''
#     获取ratings文件，设置用户信息对服装的评分
#     由于用户没有独立的信息，默认用这种方式保存用户User: name=userId, password=userId, email=userId@1.com
#     通过id对服装进行关联，设置用户对服装的评分，comment默认为空
#     '''
#     path = os.path.join(BASE, r'static\clothes\info\ratings.csv')
#     with open(path) as fb:
#         reader = csv.reader(fb)
#         # 第一排数据不用管：userId, clothesId, timestamp
#         title = reader.__next__()
#         title_dct = dict(zip(title, range(len(title))))
#         # csv文件中，一条记录就是一个用户对一件服装的评分和时间戳，一个用户可能有多条评论
#         # 所以要先取出用户所有的评分，设置成一个字典，格式为{ user:{clothes1:rating, clothes2:rating, ...}, ...}
#         user_id_dct = dict()
#         # print(title_dct)
#         for line in reader:
#             user_id = line[title_dct['userId']]
#             clothes_id = line[title_dct['clothesId']]
#             rating = line[title_dct['rating']]
#             user_id_dct.setdefault(user_id, dict())
#             user_id_dct[user_id][clothes_id] = rating
#     # 对所有用户和评分记录
#     for user_id, ratings in user_id_dct.items():
#         # 获取用户
#         u = User.objects.create(name=user_id, password=user_id, email=f'{user_id}@1.com')
#         # 必须先保存
#         u.save()
#
#
# '''
# 导入用户对服装评分
# '''
# def get_rating():
#     '''
#     获取ratings文件，设置用户信息对服装的评分
#     '''
#     path = os.path.join(BASE, r'static\clothes\info\ratings.csv')
#     with open(path) as fb:
#         reader = csv.reader(fb)
#         # 第一排数据不用管：userId, clothesId, timestamp
#         title = reader.__next__()
#         title_dct = dict(zip(title, range(len(title))))
#         # csv文件中，一条记录就是一个用户对一件服装的评分和时间戳，一个用户可能有多条评论
#         # 所以要先取出用户所有的评分，设置成一个字典，格式为{ user:{clothes1:rating, clothes2:rating, ...}, ...}
#         user_id_dct = dict()
#         # print(title_dct)
#         for line in reader:
#             user_id = line[title_dct['userId']]
#             clothes_id = line[title_dct['clothesId']]
#             rating = line[title_dct['rating']]
#             user_id_dct.setdefault(user_id, dict())
#             user_id_dct[user_id][clothes_id] = rating
#     # 对所有用户和评分记录
#     for user_id, ratings in user_id_dct.items():
#         # 获取用户
#         u = User.objects.get(name=user_id)
#         # 加入评分记录
#         for clothes_id, rating in ratings.items():
#             clothes = Clothes.objects.get(clothes_id=clothes_id)
#             relation = Clothes_rating(user=u, clothes=clothes, score=rating, comment='')
#             relation.save()
#         print(f'{user_id} process success')
#
#
# '''
# 导入服装相似度
# '''
# def calc_clothes_similarity():
#     path = os.path.join(BASE, r'static\clothes\info\clothes_similarity.csv')
#     with open(path) as fb:
#         reader = csv.reader(fb)
#         reader.__next__()
#         for line in reader:
#             # 由字符转换为值
#             line = list(map(eval, line))
#             m1,m2,val = line
#             clothes1 = Clothes.objects.get(clothes_id=m1)
#             clothes2 = Clothes.objects.get(clothes_id=m2)
#             record = Clothes_similarity(clothes_source=clothes1, clothes_target=clothes2, similarity=val)
#             record.save()
#     print("写入成功")
#
#
# '''
# 计算评分人数最多的100件服装，并存入数据库
# '''
# def clac_hot_clothes():
#     clothes = Clothes.objects.annotate(nums=Count('clothes_rating__score')).order_by('-nums')[:100]
#     # print(clothes)
#     # print(clothes.values("nums"))
#     for goods in clothes:
#         # print(goods, goods.nums)
#         record = Clothes_hot(clothes=goods, rating_number=goods.nums)
#         record.save()
#
#
# #--------------导入csv文件--------------#


class IndexView(ListView):
    model = Clothes
    template_name = 'clothing/index.html'
    paginate_by = 15
    context_object_name = 'clothes'
    ordering = 'clothes_id'
    page_kwarg = 'p'

    def get_queryset(self):
        # 返回前1000件服装
        return Clothes.objects.filter(clothes_id__lte=1000)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(*kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)
        # print(context)
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
            left_has_more = False
        else:
            left_pages = range(current_page - around_count, current_page)
            left_has_more = True

        if current_page >= paginator.num_pages - around_count - 1:
            right_pages = range(current_page + 1, paginator.num_pages + 1)
            right_has_more = False
        else:
            right_pages = range(current_page + 1, current_page + 1 + around_count)
            right_has_more = True
        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more
        }


class PopularClothesView(ListView):
    model = Clothes_hot
    template_name = 'clothing/hot.html'
    paginate_by = 15
    context_object_name = 'clothes'
    page_kwarg = 'p'

    def get_queryset(self):
        hot_clothes = Clothes_hot.objects.all().values("clothes_id")
        clothes = Clothes.objects.filter(id__in=hot_clothes).annotate(nums=Max('clothes_hot__rating_number')).order_by('-nums')
        return clothes

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PopularClothesView, self).get_context_data(*kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)
        # print(context)
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
            left_has_more = False
        else:
            left_pages = range(current_page - around_count, current_page)
            left_has_more = True

        if current_page >= paginator.num_pages - around_count - 1:
            right_pages = range(current_page + 1, paginator.num_pages + 1)
            right_has_more = False
        else:
            right_pages = range(current_page + 1, current_page + 1 + around_count)
            right_has_more = True
        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more
        }


class TagView(ListView):
    model = Clothes
    template_name = 'clothing/tag.html'
    paginate_by = 15
    context_object_name = 'clothes'
    page_kwarg = 'p'

    def get_queryset(self):
        if 'genre' not in self.request.GET.dict().keys():
            clothes = Clothes.objects.all()
            return clothes[100:200]
        else:
            clothes = Clothes.objects.filter(genre__name=self.request.GET.dict()['genre'])
            print(clothes)
            return clothes[:100]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagView, self).get_context_data(*kwargs)
        if 'genre' in self.request.GET.dict().keys():
            genre = self.request.GET.dict()['genre']
            context.update({'genre': genre})
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
            left_has_more = False
        else:
            left_pages = range(current_page - around_count, current_page)
            left_has_more = True

        if current_page >= paginator.num_pages - around_count - 1:
            right_pages = range(current_page + 1, paginator.num_pages + 1)
            right_has_more = False
        else:
            right_pages = range(current_page + 1, current_page + 1 + around_count)
            right_has_more = True
        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more
        }


class SearchView(ListView):
    model = Clothes
    template_name = 'clothing/search.html'
    paginate_by = 15
    context_object_name = 'clothes'
    page_kwarg = 'p'

    def get_queryset(self):
        clothes = Clothes.objects.filter(name__icontains=self.request.GET.dict()['keyword'])
        # print(clothes)
        return clothes

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchView, self).get_context_data(*kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)
        context.update({'keyword': self.request.GET.dict()['keyword']})
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
            left_has_more = False
        else:
            left_pages = range(current_page - around_count, current_page)
            left_has_more = True

        if current_page >= paginator.num_pages - around_count - 1:
            right_pages = range(current_page + 1, paginator.num_pages + 1)
            right_has_more = False
        else:
            right_pages = range(current_page + 1, current_page + 1 + around_count)
            right_has_more = True
        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more
        }


# 注册视图
class RegisterView(View):
    def get(self, request):
        return render(request, 'clothing/register.html')

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 格式没问题，保存
            form.save()
            return redirect(reverse('clothing:index'))
        else:
            # 表单验证失败，重定向到注册页面
            errors = form.get_errors()
            for error in errors:
                messages.info(request, error)
            # print(form.errors.get_json_data())
            return redirect(reverse('clothing:register'))


# 登录视图
class LoginView(View):
    def get(self, request):
        return render(request, 'clothing/login.html')

    def post(self, request):
        # print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('password')
            user = User.objects.filter(name=name, password=pwd).first()
            # username = form.cleaned_data.get('name')
            # print(username)
            # pwd = form.cleaned_data.get('password')
            if user:
                # 登录成功，在session 里面加上当前用户的id，作为标识
                request.session['user_id'] = user.id
                return redirect(reverse('clothing:index'))
                if remember:
                    # 设置为None，则表示使用全局的过期时间
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
            else:
                print('用户名或者密码错误')
                # messages.add_message(request,messages.INFO,'用户名或者密码错误!')
                messages.info(request, '用户名或者密码错误!')
                return redirect(reverse('clothing:login'))
        else:
            print("error!!!!!!!!!!!")
            errors = form.get_errors()
            for error in errors:
                messages.info(request, error)
            print(form.errors.get_json_data())
            return redirect(reverse('clothing:login'))


def UserLogout(request):
    # 登出，立即停止会话
    request.session.set_expiry(-1)
    return redirect(reverse('clothing:index'))

class ClothesDetailView(DetailView):
    '''
    服装详情页面
    '''
    model = Clothes
    template_name = 'clothing/detail.html'
    # 上下文对象的名称
    context_object_name = 'clothes'

    def get_context_data(self, **kwargs):
        # 重写获取上下文方法，增加评分参数
        context = super().get_context_data(**kwargs)
        # 判断是否登陆用
        login = True
        try:
            user_id = self.request.session['user_id']
        except KeyError as e:
            login = False    # 未登录

        # 获得服装的pk
        pk = self.kwargs['pk']
        clothes = Clothes.objects.get(pk=pk)

        if login:
            # 已经登录，获取当前用户的历史评分数据
            user = User.objects.get(pk=user_id)

            rating = Clothes_rating.objects.filter(user=user, clothes=clothes).first()
            # 默认值
            score = 0
            comment = ''
            if rating:
                score = rating.score
                comment = rating.comment
            context.update({'score': score, 'comment': comment})

        similarity_clothes = clothes.get_similarity()
        # 获取与当前服装最相似的服装
        context.update({'similarity_clothes': similarity_clothes})
        # 判断是否登录，没有登录则不显示评分页面
        context.update({'login': login})

        return context

    # 接收评分表单，pk是当前服装的数据库主键
    def post(self, request, pk):
        url = request.get_full_path()
        form = CommentForm(request.POST)
        if form.is_valid():
            # 获取分数和评论
            score = form.cleaned_data.get('score')
            comment = form.cleaned_data.get('comment')
            # print(score, comment)
            # 获取用户和服装
            user_id = request.session['user_id']
            user = User.objects.get(pk=user_id)
            clothes = Clothes.objects.get(pk=pk)

            # 更新一条记录
            rating = Clothes_rating.objects.filter(user=user, clothes=clothes).first()
            if rating:
                # 如果存在更新
                # print(rating)
                rating.score = score
                rating.comment = comment
                rating.save()
            else:
                # print("记录不存在")
                # 如果评分不存在
                rating = Clothes_rating(user=user, clothes=clothes, score=score, comment=comment)
                rating.save()
            messages.info(request, "评论成功!")

        else:
            # 表单没有验证成功
            messages.info(request, "评分不能为空!")
        return redirect(reverse('clothing:detail', args=(pk,)))


class RatingHistoryView(DetailView):
    '''用户详情页面'''
    model = User
    template_name = 'clothing/history.html'
    # 上下文对象的名称
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        # 这里要增加的对象：当前用户的服装历史
        context = super().get_context_data(**kwargs)
        user_id = self.request.session['user_id']
        user = User.objects.get(pk=user_id)
        # 获取ratings即可
        ratings = Clothes_rating.objects.filter(user=user)

        context.update({'ratings': ratings})
        return context


def delete_recode(request, pk):
    print(pk)
    clothes = Clothes.objects.get(pk=pk)
    user_id = request.session['user_id']
    print(user_id)
    user = User.objects.get(pk=user_id)
    rating = Clothes_rating.objects.get(user=user, clothes=clothes)
    print(clothes, user, rating)
    rating.delete()
    messages.info(request, f"删除 {clothes.name} 评分记录成功!")
    # 跳转回评分历史
    return redirect(reverse('clothing:history', args=(user_id,)))


class RecommendClothesView(ListView):
    model = Clothes
    template_name = 'clothing/recommend.html'
    paginate_by = 15
    context_object_name = 'clothes'
    ordering = 'clothes_rating__score'
    page_kwarg = 'p'

    def __init__(self):
        super().__init__()
        # 最相似的20个用户
        self.K = 20
        # 推荐出10件服装
        self.N = 10
        # 存放当前用户评分过的服装querySet
        self.cur_user_clothes_qs = None

    def get_user_sim(self):
        # 用户相似度字典，格式为{ user_id1:val , user_id2:val , ... }
        user_sim_dict = dict()
        '''获取用户之间的相似度,存放在user_sim_dct中'''
        # 获取当前用户
        cur_user_id = self.request.session['user_id']
        cur_user = User.objects.get(pk=cur_user_id)
        # 获取其他用户
        other_users = User.objects.exclude(pk=cur_user_id)

        self.cur_user_clothes_qs = Clothes.objects.filter(user=cur_user)

        # 计算当前用户与其他用户评分过的服装交集数
        for user in other_users:
            # 记录感兴趣的数量
            user_sim_dict[user.id] = len(Clothes.objects.filter(user=user) & self.cur_user_clothes_qs)

        # 按照key排序value，返回K个最相似的用户
        print('user similarity calculated!')
        # 格式是 [ (user, value), (user, value), ... ]
        return sorted(user_sim_dict.items(), key=lambda x: -x[1])[:self.K]

    def get_recommend_clothes(self, user_lst):
        # 服装兴趣值字典，{ clothes:value, clothes:value , ...}
        clothes_val_dct = dict()
        # 用户，相似度
        for user, _ in user_lst:
            # 获取相似用户评分过的电影，并且不在前用户的评分列表中的，再加上score字段，方便计算兴趣值
            clothes_set = Clothes.objects.filter(user=user).exclude(id__in=self.cur_user_clothes_qs).annotate(
                score=Max('clothes_rating__score'))
            for goods in clothes_set:
                clothes_val_dct.setdefault(goods, 0)
                # 累计用户的评分
                clothes_val_dct[goods] += goods.score
        print('recommend clothes list calculated!')
        return sorted(clothes_val_dct.items(), key=lambda x: -x[1])[:self.N]

    def get_queryset(self):
        s = time.time()
        # 获得最相似的K个用户列表
        user_lst = self.get_user_sim()
        # 获得推荐服装的id
        clothes_lst = self.get_recommend_clothes(user_lst)
        print(clothes_lst)
        result_lst = []
        for goods, _ in clothes_lst:
            result_lst.append(goods)
        e = time.time()
        print(f"用时:{e - s}")
        return result_lst

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RecommendClothesView, self).get_context_data(*kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
            left_has_more = False
        else:
            left_pages = range(current_page - around_count, current_page)
            left_has_more = True

        if current_page >= paginator.num_pages - around_count - 1:
            right_pages = range(current_page + 1, paginator.num_pages + 1)
            right_has_more = False
        else:
            right_pages = range(current_page + 1, current_page + 1 + around_count)
            right_has_more = True
        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more
        }
