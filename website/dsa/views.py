import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .models import Comment, Feedback, FeedbackOption


# Create your views here.
class HomeView(TemplateView):
	template_name = "public/home.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			feedbacks = Feedback.objects.filter(user=self.request.user).exclude(no_vote=True)
			if len(feedbacks) > 0:
				context["feedbacks"] = feedbacks
		feedback_options = FeedbackOption.objects.all()
		context["feedback_options"] = feedback_options

		return context


class VoteView(LoginRequiredMixin, TemplateView):
	template_name = "dsa/vote.html"

	def get_context_data(self, **kwargs):
		selected_statuses = kwargs.pop("selected_statuses", {})
		selected_options = kwargs.pop("selected_options", {})
		vote_errors = kwargs.pop("vote_errors", {})
		context = super().get_context_data(**kwargs)
		context["llang"] = "ar"
		context["selected_statuses"] = selected_statuses
		context["selected_options"] = selected_options
		context["vote_errors"] = vote_errors

		feedback_options = FeedbackOption.objects.all()
		context["feedback_options"] = feedback_options


		feedbacks = Feedback.objects.filter(user=self.request.user).exclude(no_vote=False)
		if len(feedbacks) > 0:
			context["unvoted"] = feedbacks
			return context
		

		# Comments the user hasn't voted on yet
		feedbacks = Feedback.objects.all()
		unvoted = Comment.objects.exclude(feedbacks__in=feedbacks)

		commits_per_page = 3

		context["unvoted"] = []
		for limit in range(0, commits_per_page):
			new_feedback = Feedback(comment=unvoted[limit], user=self.request.user)
			new_feedback.save()
			context["unvoted"].append(new_feedback)

		return context

	@transaction.atomic
	def post(self, request, *args, **kwargs):
		compiler = re.compile(r'^status_(\d+)$')
		updates = []
		selected_statuses = {}
		selected_options = {}
		vote_errors = {}

		for key in request.POST.keys():
			match = compiler.match(key)
			if not match:
				continue

			feedback_id = int(match.group(1))
			status = request.POST.get(key)
			selected_statuses[feedback_id] = status
			option_ids = []
			for option_id in request.POST.getlist(f"vote_{feedback_id}"):
				try:
					option_ids.append(int(option_id))
				except (TypeError, ValueError):
					continue
			selected_options[feedback_id] = option_ids
			try:
				feedback = Feedback.objects.get(pk=feedback_id, user=request.user)
			except Feedback.DoesNotExist:
				continue

			if status == "hasProblems" and not option_ids:
				vote_errors[feedback_id] = "At least one problem type must be selected."

			updates.append((feedback, status, option_ids))

		if vote_errors:
			context = self.get_context_data(
				selected_statuses=selected_statuses,
				selected_options=selected_options,
				vote_errors=vote_errors,
			)
			return self.render_to_response(context)

		valid_option_ids = set(FeedbackOption.objects.values_list("id", flat=True))
		for feedback, status, option_ids in updates:
			feedback.options.clear()

			if status == "novote":
				feedback.no_vote = True
				feedback.normal = False
				feedback.hate_speech = False
			elif status == "normal":
				feedback.no_vote = False
				feedback.normal = True
				feedback.hate_speech = False
			elif status == "hasProblems":
				feedback.no_vote = False
				feedback.normal = False
				feedback.hate_speech = True
			else:
				continue

			feedback.save()

			if status == "hasProblems":
				feedback.options.add(*[option_id for option_id in option_ids if option_id in valid_option_ids])

		return redirect("vote")