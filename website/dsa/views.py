import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Count
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .models import Comment, Feedback


# Create your views here.
class HomeView(TemplateView):
	template_name = "public/home.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		ranked_users = list(
			Feedback.objects.filter(score__gt=0)
			.values("user_id", "user__email", "user__full_name")
			.annotate(votes=Count("id"))
			.order_by("-votes", "user__email")
		)

		top_limit = 10
		leaderboard = []
		current_user_row = None

		for index, row in enumerate(ranked_users, start=1):
			entry = {
				"rank": index,
				"user_id": row["user_id"],
				"display_name": row["user__full_name"] or row["user__email"],
				"email": row["user__email"],
				"votes": row["votes"],
				"is_current_user": self.request.user.is_authenticated and row["user_id"] == self.request.user.pk,
			}

			if index <= top_limit:
				leaderboard.append(entry)

			if entry["is_current_user"]:
				current_user_row = entry

		context["leaderboard"] = leaderboard
		context["current_user_row"] = current_user_row
		context["show_current_user_separate"] = bool(
			current_user_row and current_user_row["rank"] > top_limit
		)

		return context


class VoteView(LoginRequiredMixin, TemplateView):
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