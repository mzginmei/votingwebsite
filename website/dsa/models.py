from django.conf import settings
from django.db import models


"""
Revised on 2026-04-09
Regarding Issue #1

[0] No Vote
[1] Normal 
[2]     
[3] وشەی نەشیاو/ سێکسیزم
[4] وشەی ناشرین/ جنێو
[5] ڕەخنەی ڕووخێنەر
[6] گەڤ (هەڕەشەی کەسی)
[7] نەرێنی
[8] دڵتەنگی/ خەم و خەفەت
[9] ترس و تۆقاندن
[10] توانج/ تعلیق
"""

# FEEDBACK_CHOICES = (
#     (0, 'No Vote'),
#     (1, 'Normal'),
#     (2, 'ڕەگەزپەرستی/ نەتەوەپەرستی'),
#     (3, 'وشەی نەشیاو/ سێکسیزم'),
#     (4, 'وشەی ناشرین/ جنێو'),
#     (5, 'ڕەخنەی ڕووخێنەر'),
#     (6, 'گەڤ (هەڕەشەی کەسی)'),
#     (7, 'نەرێنی'),
#     (8, 'دڵتەنگی/ خەم و خەفەت'),
#     (9, 'ترس و تۆقاندن'),
#     (10, 'توانج/ تعلیق'),
# )


# Create your models here.
class Comment(models.Model):
    text = models.TextField()


class FeedbackOption(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='feedbacks')
    no_vote = models.BooleanField(default=True)
    normal = models.BooleanField(default=False)
    hate_speech = models.BooleanField(default=False)
    options = models.ManyToManyField(FeedbackOption, blank=True)