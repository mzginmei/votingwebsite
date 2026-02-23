import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .models import Comment, Feedback


# Create your views here.
class HomeView(TemplateView):
	template_name = "public/home.html"


class VoteView(TemplateView, LoginRequiredMixin):
	template_name = "dsa/vote.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		feedbacks = Feedback.objects.filter(user=self.request.user).exclude(score__gt=0)
		if len(feedbacks) > 0:
			context["unvoted"] = feedbacks
			return context

		# Comments the user hasn't voted on yet
		feedbacks = Feedback.objects.all()
		unvoted = Comment.objects.exclude(feedbacks__in=feedbacks)

		context["unvoted"] = []
		for limit in range(0, 10):
			new_feedback = Feedback(comment=unvoted[limit], user=self.request.user)
			new_feedback.save()
			context["unvoted"].append(new_feedback)

		# done = Feedback.objects.filter(user=self.request.user)
		# context["voted"] = len(done)

		return context

	@transaction.atomic
	def post(self, request, *args, **kwargs):

		compiler = re.compile(r'vote_(\d+)')
		for key, value in request.POST.items():
			if not compiler.match(key):
				continue
			feedback_id = int(key.split("_")[1])
			try:
				feedback = Feedback.objects.get(pk=feedback_id)
				feedback.score = 1 if value == "nohate" else 2
				feedback.save()
			except Feedback.DoesNotExist:
				continue

		return redirect("vote")