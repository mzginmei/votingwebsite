from django.conf import settings
from django.db import models


# Create your models here.
class Comment(models.Model):
    text = models.TextField()


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='feedbacks')
    score = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        if self.score == 0:
            return f'{self.user.email} - no vote yet'
        elif self.score == 1:
            return f'{self.user.email} - voted no hate'
        else:
            return f'{self.user.email} - voted hate'

