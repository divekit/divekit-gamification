from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from .scripts import dkb
from .models import DKBFile

class BadgeRuleView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request:Request, *args, **kwargs):
        dkb_object = DKBFile.objects.get(pk=kwargs.get("dkbfile_id"))
        
        if(dkb_object.text):
            # print(dkb_object.text)
            lines = dkb_object.text
        else:
            try:
                file = dkb_object.file
                file.open(mode="r")
                lines = file.read()
            finally:
                file.close()

        try:
            dkb.run(lines,request.data)
        except Exception as e:
            return Response(
                {
                    "error":{
                        "type":"runtime",
                        "msg":str(e)
                        }
                }
                ,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
    