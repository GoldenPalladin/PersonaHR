from django.shortcuts import redirect


def redirect_to_docs(request):
    response = redirect('/docs/')
    return response
