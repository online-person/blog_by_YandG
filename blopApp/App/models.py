import hashlib

from django.db import models

# Create your models here.
class UserModel(models.Model):
    u_name = models.CharField(max_length=20,unique=True)
    u_icon = models.CharField(max_length=150)
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=32)
    is_del = models.BooleanField(default=False)
    is_act = models.BooleanField(max_length=False)

    def set_pwd(self,pwd):
        self.u_password = self.generate_pwd(pwd)

    def generate_pwd(self,pwd):
        sha = hashlib.sha512()
        sha.update(pwd.encode("utf-8"))
        return sha.hexdigest

    def verify_pwd(self,pwd):
        return self.u_password == self.generate_pwd(pwd)
