# from django.conf.urls import url
from django.urls import re_path
from django.views.generic import View

class TestView(View):

    def get(self, request):
        from django.http import HttpResponse

        return HttpResponse('ok')

urlpatterns = [
    re_path('^test$', TestView.as_view()),
]
