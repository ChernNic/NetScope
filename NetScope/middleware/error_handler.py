from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class CustomErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if settings.DEBUG:
            return None
        return render(request, "errors/500.html", {"message": str(exception)}, status=500)