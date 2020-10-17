from django.shortcuts import redirect


def redirect_to_docs(request):
    response = redirect('/docs/')
    return response

def redirect_to_questions(request):
    response = redirect('/api/questions')
    return response