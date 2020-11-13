from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from typing import List, Tuple, Optional

SwaggerDetails = List[Tuple[str, str, str, List[str], Optional[List[
    Parameter]]]]


class SwaggedViewSet(viewsets.ModelViewSet):
    """
    params = query parameter names, must be of equal match with
    table fields
    """
    http_method_names = ['get', 'post', 'put', 'head']
    params = []

    def update(self, request, *args, **kwargs):
        kwargs.update({'partial': True})
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        """
        Determine which serializer to user `list` or `detail`
        """
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class

        return super().get_serializer_class()

    def get_queryset(self):

        queryset = self.queryset
        for param in self.params:
            param_value = self.request.query_params.get(param, None)
            if param_value:
                queryset = queryset.filter(**{param: param_value})
        return queryset


def add_swagger(swagger_details: SwaggerDetails):
    """
    let's decorate ecorating decoratod into decorator
    :param swagger_details: tuple of method_name, operation_id,
    operation_decsription, [tags], [params]
    :return:
    """
    def decorate(cls):
        for detail in swagger_details:
            method_name, op_id, op_decsr, tags, params = detail
            swagger_decorator = swagger_auto_schema(operation_id=op_id,
                                                    operation_description=op_decsr,
                                                    tags=tags,
                                                    manual_parameters=params)
            dec = method_decorator(decorator=swagger_decorator,
                                   name=method_name)
            cls = dec(cls)
        return cls
    return decorate
