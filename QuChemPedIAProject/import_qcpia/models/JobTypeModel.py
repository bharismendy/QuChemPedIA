from django.db import models


class JobType(models.Model):
    """this class define the table where the name of job_type are stored"""
    id_job_type = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10, default=None, null=False)

    class meta:
        verbose_name = "Software"

    def __str__(self):
        return str(self.id_job_type)
