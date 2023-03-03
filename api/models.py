from django.db import models


# Create your models here.
class Favorite(models.Model):
    teamId = models.IntegerField(unique=True, blank=False, null=False)
    nameTeams = models.CharField(max_length=250, blank=True, null=False)
    seraial = models.CharField(max_length=250, blank=True, null=True)
    user = models.CharField(max_length=60, blank=True, null=True)
    isFavorite = models.BooleanField(verbose_name='favorito')

    def __str__(self):
        return self.nameTeams

    def toJSON(self):
        item = models_to_dict(self)
        return item

    class Meta:
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'
        db_table = 'favorite'
        ordering = ['id']
