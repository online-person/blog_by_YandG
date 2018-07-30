import hashlib

from datetime import datetime
from django.db import models

# 用户权限说明
# 1 阅读
# 2 发帖
# 3 删自己的帖子或者修改
# 4 删别人的帖子，置顶帖子,恢复帖子 ，删除不当言论 管理者
# 5 最高权限 boss
READ_POWER = 1
WRITE_POWER = 2
MODIFY_POWER  = 3
TALLER_MODIFY_POWER = 4
TALLER_POWER = 5


def authority(auth):  # 帖子相关权限验证
    def wrapper(func):
        def inner(*args, **kwargs):
            post, request = args[:2]
            user_id = request.session.get('user_id')
            user = UserModel.objects.filter(id=user_id).first()

            if (post.p_user == user):
                if user.u_authority < auth:
                    return "you has not authority",403
                func(*args,**kwargs)
            else:
                if user.u_authority <= auth:
                    return "you has not authority",403
                func(*args, **kwargs)
        return inner
    return wrapper

class UserModel(models.Model):
    u_name = models.CharField(max_length=20,unique=True)
    u_icon = models.ImageField(upload_to="icons")
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=32)
    u_authority = models.IntegerField(default=READ_POWER)   # 用户权限
    is_del = models.BooleanField(default=False)
    is_act = models.BooleanField(default=False)


    def set_pwd(self,pwd):
        self.u_password = self.generate_pwd(pwd)

    def generate_pwd(self,pwd):
        sha = hashlib.sha512()
        sha.update(pwd.encode("utf-8"))
        return sha.hexdigest()

    def verify_pwd(self,pwd):
        return self.u_password == self.generate_pwd(pwd)

    def isdel(self):
        pass

class PostModel(models.Model):
    p_title = models.CharField(max_length=100)  # 标题
    p_comment = models.TextField()              # 内容
    is_del = models.BooleanField(default=False)  # 是否删除
    p_user = models.ForeignKey(UserModel, default=0)
    p_created = models.DateTimeField(auto_now_add=datetime.now())
    p_update = models.DateTimeField(auto_now=datetime.now())

    @authority(MODIFY_POWER)  # 验证删除权限
    def deleted(self,request):
        self.is_del = True
        self.save()

    @authority(TALLER_MODIFY_POWER)
    def recovery(self,request):
        self.is_del = False
        self.save()

    @authority(MODIFY_POWER)  # 验证修改权限
    def modify(self,request):
        self.p_comment = request.POST.get("content")
        self.p_title = request.POST.get("title")
        self.save()

    def create_post(self,user,POST):
        self.p_title = POST.get("title")
        self.p_comment = POST.get("content")
        self.p_user = user
        self.save()

    def toDict(self):
        return {
            'title': self.p_title,
            'user': self.p_user.u_name,
            'content': self.p_comment,
            'create_time': self.p_created,
            'update_time': self.p_update,
            'post_id':self.id
        }




class PostList(models.Model):
    pl_post = models.ForeignKey(PostModel)
    pl_user = models.ForeignKey(UserModel)
