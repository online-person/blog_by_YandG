import hashlib

from datetime import datetime
from django.db import models

# 用户权限说明
# 0 阅读
# 1 发帖
# 2 删自己的帖子或者修改
# 3 删别人的帖子，置顶帖子 ，删除不当言论 管理者
# 4 最高权限 boss
READ_POWER = 1
WRITE_POWER = 2
MODIFY_POWER  = 3
TALLER_MODIFY_POWER = 4
TALLER_POWER = 5


def authority(auth):  # 帖子相关权限验证
    def wrapper(func):
        def inner(*args, **kwargs):
            post, user_id = args[:2]
            user = UserModel.objects.filter(id=user_id).first()
            if post.p_user == user:
                if user.u_authority < auth:
                    return "you has not authority"
                func(*args,**kwargs)
            else:
                if user.u_authority <= auth:
                    return "you has not authority"
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
        return sha.hexdigest

    def verify_pwd(self,pwd):
        return self.u_password == self.generate_pwd(pwd)

    def isdel(self):
        pass

class PostModel(models.Model):
    p_title = models.CharField(max_length=100)  # 标题
    p_comment = models.TextField()              # 内容
    is_del = models.BooleanField(max_length=False)  # 是否删除
    p_user = models.ForeignKey(UserModel, default=0)
    p_created = models.DateTimeField(auto_now_add=datetime.now())
    p_update = models.DateTimeField(auto_now=datetime.now())

    @authority(MODIFY_POWER)  # 验证删除权限
    def del_post(self,u_id):
        self.is_del = True
        self.save()

    @authority(MODIFY_POWER)  # 验证修改权限
    def modify_post(self,u_id,data):
        self.p_comment = data
        self.save()

    @authority(WRITE_POWER)  # 验证写权限
    def create_post(self,u_id,data=None):
        self.p_title = data.title
        self.p_comment = data.comment
        self.p_user = data.user





class PostList(models.Model):
    pl_post = models.ForeignKey(PostModel)
    pl_user = models.ForeignKey(UserModel)
