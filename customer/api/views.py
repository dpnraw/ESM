from rest_framework.generics import ListAPIView

from customer.models import Customer

from .serializers import CustomerLocationSerializer


class CustomerLocationView(ListAPIView):

    queryset = Customer.objects.all()
    serializer_class = CustomerLocationSerializer
    http_method_names = [
        'get',
        'head',
        'options',
    ]
