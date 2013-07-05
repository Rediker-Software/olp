class PatchModelsMiddleware(object):

    def __init__(self):
        from django.core.exceptions import MiddlewareNotUsed
        from .utils import patch_models

        patch_models()

        raise MiddlewareNotUsed()
