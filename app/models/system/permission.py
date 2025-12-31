from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 权限表
class PermissionManager(models.Manager):
    def add(self, role_id, permission):
        return self.create(role_id=role_id, permission=permission)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def deleteByRole(self, role_id):
        return self.filter(role_id=role_id).delete()
    
    def getList(self, role_id):
        return self.filter(role_id=role_id)

    def encoderList(self, permissions):
        return [model_to_dict(permission, fields=['id', 'role_id', 'permission']) for permission in permissions]
    
class Permission(models.Model):
    objects = PermissionManager()
    role_id = models.IntegerField(db_index = True) # 角色id
    permission = models.IntegerField(db_index = True) # 权限
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_permission'
