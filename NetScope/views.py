from django.shortcuts import render

def handler404(request, exception, *args, **kwargs):
    return render(request, "errors/404.html", status=404)

def handler403(request, exception, *args, **kwargs):
    return render(request, "errors/403.html", status=403)