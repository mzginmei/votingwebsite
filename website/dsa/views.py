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
			Feedback.objects.filter(no_vote=False)
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
		context["llang"] = "ar"

		feedbacks = Feedback.objects.filter(user=self.request.user).exclude(no_vote=False)
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

		compiler = re.compile(r'^status_(\d+)$')
		for key in request.POST.keys():
			match = compiler.match(key)
			if not match:
				continue

			feedback_id = int(match.group(1))
			status = request.POST.get(key)
			try:
				feedback = Feedback.objects.get(pk=feedback_id, user=request.user)
			except Feedback.DoesNotExist:
				continue
			
			if status == "normal":
				feedback.score_1 = True	
				feedback.no_vote = False

				feedback.score_2 = False
				feedback.score_3 = False
				feedback.score_4 = False
				feedback.score_5 = False
				feedback.score_6 = False
				feedback.score_7 = False
				feedback.score_8 = False
				feedback.score_9 = False
				feedback.score_10 = False

			elif status == "no_vote":
				feedback.no_vote = True
				feedback.score_1 = False
				feedback.score_2 = False
				feedback.score_3 = False
				feedback.score_4 = False
				feedback.score_5 = False
				feedback.score_6 = False
				feedback.score_7 = False
				feedback.score_8 = False
				feedback.score_9 = False
				feedback.score_10 = False


			else:
				selected = request.POST.getlist(f"vote_{feedback_id}")
				feedback.no_vote = False
				feedback.score_1 = False
				for s in selected:
					if s == "2":
						feedback.score_2 = True
					elif s == "3":
						feedback.score_3 = True
					elif s == "4":
						feedback.score_4 = True
					elif s == "5":
						feedback.score_5 = True
					elif s == "6":
						feedback.score_6 = True
					elif s == "7":
						feedback.score_7 = True
					elif s == "8":
						feedback.score_8 = True
					elif s == "9":
						feedback.score_9 = True
					elif s == "10":
						feedback.score_10 = True

				

			feedback.save()

		return redirect("vote")