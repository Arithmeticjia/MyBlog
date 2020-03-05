from django.db import models


class System_Monit(models.Model):
    # id自增,类型为bigint。设置为主键
    id = models.BigAutoField(primary_key=True)
    # 类型为decimal(10,2)，长度为10，小数点保留2位
    cpu = models.DecimalField(max_digits=10, decimal_places=2)
    # 类型为int(11)，11是默认长度
    cur_mem = models.IntegerField()
    mem_rate = models.DecimalField(max_digits=10, decimal_places=2)
    mem_all = models.IntegerField()
    # 类型为datetime
    create_time = models.DateTimeField()
    # 由于毫秒的时间戳超过了timestamp的长度，所以只能设置bigint了。
    time_stamp = models.BigIntegerField()

# Create your models here.
