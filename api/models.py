from django.contrib.auth.models import User
from django.db import models
# Create your models here.



class Reports(models.Model):
	industory1 = models.TextField(null= True, blank= True)
	year1 = models.TextField(null= True, blank= True)
	month1 = models.TextField(null= True, blank= True)
	kam1 = models.TextField(null= True, blank= True)
	product_type1 = models.TextField(null= True, blank= True)
	product1 = models.TextField(null= True, blank= True)
	industory2 = models.TextField(null= True, blank= True)
	year2 = models.TextField(null= True, blank= True)
	month2 = models.TextField(null= True, blank= True)
	kam2 = models.TextField(null= True, blank= True)
	product_type2 = models.TextField(null= True, blank= True)
	product2 = models.TextField(null= True, blank= True)
	report_name = models.CharField(max_length=100, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null= True, blank= True)

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name_plural = "Reports"
