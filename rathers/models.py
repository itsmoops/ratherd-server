from django.db import models

# Create your models here.
class Rather(models.Model):
	rather_text = models.CharField(max_length=1000)
	wins = models.IntegerField(default=0)
	losses = models.IntegerField(default=0)
	ratio = models.DecimalField(default=0.5, max_digits=20, decimal_places=10)
	is_pair = models.BooleanField(default=False)
	paired_id = models.IntegerField(default=0)
	date_submitted = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.rather_text

	def save(self, *args, **kwargs):
		if self.wins > 0 or self.losses > 0:
			self.ratio = round(float(self.wins) / (float(self.wins) + float(self.losses)), 10)
		else:
			self.ratio = 0.5
		print(self.ratio)
		super(Rather, self).save(*args, **kwargs)
	