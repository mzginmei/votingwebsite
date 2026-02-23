from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Comment(models.Model):
    text = models.TextField()


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='feedbacks')
    score = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        if self.score == 0:
            return f'{self.user.username} - no vote yet'
        elif self.score == 1:
            return f'{self.user.username} - voted no hate'
        else:
            return f'{self.user.username} - voted hate'

