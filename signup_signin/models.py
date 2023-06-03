from django.db import models


class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64)
    date = models.DateField()
    task = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task} - {self.completed}"