from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def root_route(request):
    """
    Main view for landing api page
    instead of having not found error
    """
    return Response({
        "message": "Welcome to arthub_api!"
    })
