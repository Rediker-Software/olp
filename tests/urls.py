from django.conf.urls import url
from django.views.generic import View

class TestView(View):

    def get(self, request):
        from django.http import HttpResponse

        return HttpResponse('ok')

urlpatterns = [
    url('^test$', TestView.as_view()),
]
