import hashlib

from django.db import models

# 用户权限说明
# 0 阅读
# 1 发帖
# 2 删自己的帖子或者修改
# 3 删别人的帖子，置顶帖子 ，删除不当言论 管理者
# 4 最高权限 boss
READ_POWER = 0
WRITE_POWER = 1
DEL_SELF_POWER  = 2
DEL_OTHER_POWER = 3
TALLER_POWER = 4

# Create your models here.
class PostModel(models.Model):
    p_title = models.CharField(max_length=100)  # 标题
    p_owner = models.CharField(max_length=20)  # 所有者
    p_comment = models.TextField()              # 内容
    is_del = models.BooleanField(max_length=False)  # 是否删除


    def del_post(self,u_name):
        user = UserModel.objects.get(u_name=u_name)
        post_owner = UserModel.objects.get(u_name=self.p_owner)

        if u_name == self.p_owner:
            return "del ok"
        elif user.u_authority > post_owner.u_authority:
            return "del ok"
        else:
            return "del failed"


class UserModel(models.Model):
    u_name = models.CharField(max_length=20,unique=True)
    u_icon = models.ImageField(upload_to="icons")
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=32)
    u_authority = models.IntegerField(default=READ_POWER)   # 用户权限
    u_posts = models.ForeignKey(PostModel,default=0)
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


class PostList(models.Model):
    pl_name = models.CharField(max_length=100)
    pl_user = models.CharField(max_length=20)
    pl_user_icon = models.CharField(max_length=100)
