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

		# Comments the user hasn't voted on yet
		feedbacks = Feedback.objects.all()
		unvoted = Comment.objects.exclude(feedbacks__in=feedbacks)

		context["unvoted"] = []
		for limit in range(0, 10):
			context["unvoted"].append(unvoted[limit])

		done = Feedback.objects.filter(user=self.request.user)
		context["voted"] = len(done)

		return context

	@transaction.atomic
	def post(self, request, *args, **kwargs):

		compiler = re.compile(r'vote_(\d+)')
		for key, value in request.POST.items():
			if not compiler.match(key):
				continue
			comment_id = int(key.split("_")[1])
			print (comment_id, value)
			try:
				comment = Comment.objects.get(pk=comment_id)
				feedback = Feedback(comment=comment, user=request.user)
				feedback.score = 0 if value == "no" else 1
				feedback.save()
			except Comment.DoesNotExist:
				continue

		print (request.POST)
		return redirect("vote")