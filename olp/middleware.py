# class PatchModelsMiddleware(object):

#     def __init__(self):
#         from django.core.exceptions import MiddlewareNotUsed
#         from .utils import patch_models

#         patch_models()

#         raise MiddlewareNotUsed()

from django.core.exceptions import MiddlewareNotUsed
from .utils import patch_models


class PatchModelsMiddleware:
    def __init__(self, get_response):
        # Accepting the get_response parameter as required by Django
        self.get_response = get_response

        # Call the patch_models function
        patch_models()

        # Optionally raise MiddlewareNotUsed to stop further processing
        raise MiddlewareNotUsed("PatchModelsMiddleware has been used")

    def __call__(self, request):
        # This is where the actual middleware chain happens.
        # The middleware does not process the request any further
        # due to the `MiddlewareNotUsed` raised in __init__.
        return self.get_response(request)

