try:
    from django.conf.urls import include, patterns, url
except ImportError:
    from django.conf.urls.defaults import include, patterns, url

from olp.utils import patch_user


patch_user()

urlpatterns = patterns('',
    
)
