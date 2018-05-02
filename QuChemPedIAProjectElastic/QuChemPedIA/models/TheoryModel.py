from django.db import models


class theory(models.Model):
    # data about the user
    id_theory = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10, default=None)

    class Meta:
        verbose_name = "theory"

    def __str__(self):
        return self.name