from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MatchSerializer

import sys
from answers.models import Answers

def match_spec():
    #r = [{"pk": 10, "name": '0'}, {"pk": 4, "name": '23'}]
    r = Answers.objects.filter(specialization=1)
    sys.stderr.write(str(r[0].added))
    r = [{"pk": 10, "name": '0'}, {"pk": 4, "name": '23'}]
    return(r)


@api_view(['GET'])
def match_list(request):
    if request.method == 'GET':
        match_results = match_spec()
        results = MatchSerializer(match_results, many=True).data
        return Response(results)
	
'''
from rest_framework import views
from rest_framework.response import Response
from .serializers import MatchSerializer

class MatchView(views.APIView):

    def get(self, request):
        match_results= [{"likes": 10, "comments": 0}, {"likes": 4, "comments": 23}]
        results = MatchSerializer(match_results, many=True).data
        return Response(results)
'''