from django.db import models


class functionnal(models.Model):
    # data about the user
    id_functionnal = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15, default=None)

    class Meta:
        verbose_name = "functionnal"

    def __str__(self):
        return self.name