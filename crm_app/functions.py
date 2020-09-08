from rest_framework import status
from rest_framework.response import Response
# Create your views here.
def HandleResponse(data,message,success = True,err = 'no err',resp_status = status.HTTP_200_OK):
    """
    HandleResponse , makes easier to send Response
    Equalent to Response({
            'success':success,
            "error":err,
            "message":message,
            "data":data
        },status = resp_status)
    """
    return Response({
        'success':success,
        "error":err,
        "message":message,
        "data":data
    },status = resp_status)
