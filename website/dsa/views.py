import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Count
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
		context = super().get_context_data(**kwargs)
		context["llang"] = "ar"

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
		for key in request.POST.keys():
			match = compiler.match(key)
			if not match:
				continue

			feedback_id = int(match.group(1))
			status = request.POST.get(key)
			try:
				feedback = Feedback.objects.get(pk=feedback_id, user=request.user)
				print ("found feedback for user", request.user, "and comment", feedback.comment)
			except Feedback.DoesNotExist:
				continue
			
			if status == "novote":
				print ("setting no vote for feedback", feedback_id)
				feedback.no_vote = True
				feedback.normal = False
				feedback.hate_speech = False
				feedback.options.clear()
				feedback.save()
			
			elif status == "normal":
				print ("setting normal for feedback", feedback_id)
				feedback.no_vote = False
				feedback.normal = True
				feedback.hate_speech = False
				feedback.options.clear()
				feedback.save()
			
			elif status == "hasProblems":
				print ("setting has problems for feedback", feedback_id)
				feedback.no_vote = False
				feedback.normal = False
				feedback.hate_speech = True
				feedback.options.clear()


				for option_id in request.POST.getlist(f"vote_{feedback_id}"):
					try:
						option = FeedbackOption.objects.get(pk=int(option_id))
						print ("adding option", option, "to feedback", feedback_id)
						feedback.options.add(option)
						feedback.save()
					except FeedbackOption.DoesNotExist:
						continue

			else:
				pass	

			feedback.save()

		return redirect("vote")