from django.shortcuts import redirect


def redirect_view(request):
    response = redirect('/docs/')
    return response

