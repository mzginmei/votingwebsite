from django.views.generic import TemplateView


class Custom404View(TemplateView):
	template_name = "error/404.html"


class Custom403View(TemplateView):
	template_name = "error/403.html"


class Custom500View(TemplateView):
	template_name = "error/500.html"
