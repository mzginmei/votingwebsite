from django.conf import settings
from django.db import models


"""
Revised on 2026-04-09
Regarding Issue #1

[0] No Vote
[1] Normal 
[2] ڕەگەزپەرستی/ نەتەوەپەرستی
[3] وشەی نەشیاو/ سێکسیزم
[4] وشەی ناشرین/ جنێو
[5] ڕەخنەی ڕووخێنەر
[6] گەڤ (هەڕەشەی کەسی)
[7] نەرێنی
[8] دڵتەنگی/ خەم و خەفەت
[9] ترس و تۆقاندن
[10] توانج/ تعلیق
"""

FEEDBACK_CHOICES = (
    (0, 'No Vote'),
    (1, 'Normal'),
    (2, 'ڕەگەزپەرستی/ نەتەوەپەرستی'),
    (3, 'وشەی نەشیاو/ سێکسیزم'),
    (4, 'وشەی ناشرین/ جنێو'),
    (5, 'ڕەخنەی ڕووخێنەر'),
    (6, 'گەڤ (هەڕەشەی کەسی)'),
    (7, 'نەرێنی'),
    (8, 'دڵتەنگی/ خەم و خەفەت'),
    (9, 'ترس و تۆقاندن'),
    (10, 'توانج/ تعلیق'),
)


# Create your models here.
class Comment(models.Model):
    text = models.TextField()


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='feedbacks')
    no_vote = models.BooleanField(default=True)
    score_1 = models.BooleanField(default=False)
    score_2 = models.BooleanField(default=False)
    score_3 = models.BooleanField(default=False)
    score_4 = models.BooleanField(default=False)
    score_5 = models.BooleanField(default=False)
    score_6 = models.BooleanField(default=False)
    score_7 = models.BooleanField(default=False)
    score_8 = models.BooleanField(default=False)
    score_9 = models.BooleanField(default=False)
    score_10 = models.BooleanField(default=False)