from __future__ import unicode_literals
from random import random
import string
import time
from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=50L)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        db_table = 'product'


class OrderManager(models.Manager):

    def create_order(self):

        order = self.model()
        order.order_number = OrderManager._generate_order_id()
        order.status = Order.ORDER_STATUS_NEW
        order.save()

        return order

    @staticmethod
    def _generate_order_id():

        """
        ORDER NUM = RAMDOM CHARACTER(5) + TIME MILLISECONDS FOR DATE TIME (10 DIGITS)
        """
        current_milli_time = str(int(round(time.time())))
        rand_str = OrderManager._random_string_generator()

        return '%s%s' % (rand_str, current_milli_time)

    @staticmethod
    def _random_string_generator(size=4, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))


class Order(models.Model):

    ORDER_STATUS_NEW = 0
    ORDER_STATUS_READY = 1

    id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=20L)
    regular_price = models.IntegerField(null=True, blank=True, default=0)
    actual_price = models.IntegerField(null=True, blank=True, default=0)
    status = models.IntegerField(null=True, default=0)
    modify_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    object = OrderManager()

    class Meta:
        db_table = 'order'


class OrderDetailManager(models.Manager):

    def purchase_item(self, order_number, product_code, amount):

        order = Order.objects.get(order_number=order_number)
        product = Product.objects.get(product_code=product_code)

        od = self.model()
        od.order = order
        od.product = product
        od.unit_price = product.price
        od.amount = amount
        od.regular_price = product.price * amount
        od.save()


class OrderDetail(models.Model):

    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name="details")
    product = models.ForeignKey('Product')
    amount = models.IntegerField()
    unit_price = models.IntegerField()
    regular_price = models.IntegerField()
    actual_price = models.IntegerField()

    object = OrderDetailManager()

    class Meta:
        db_table = 'order_detail'


class OrderPromotionLog(models.Model):
    id = models.AutoField(primary_key=True)
    promotion = models.ForeignKey('Promotion', blank=True, null=True)
    order = models.ForeignKey(Order, null=True, blank=True)
    order_detail = models.ForeignKey(OrderDetail, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    promotion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'order_promotion_log'


class Promotion(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50)
    rule_script = models.TextField()
    description = models.CharField(max_length=500)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'promotion'
