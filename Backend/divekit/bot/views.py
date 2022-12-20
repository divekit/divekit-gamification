
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsStaffOrReadOnly, IsStaffOrSelf,IsStaff
from .models import Verification
from .serializers import VerificationSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample



class VerificationsListView(APIView):
    permission_classes = (IsStaffOrReadOnly,)
    
    @extend_schema(
        tags=["bot"]
    )
    def get(self,request,*args,**kwargs):
        verifications = Verification.objects.all()
        serializer = VerificationSerializer(verifications,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["bot"]
    )
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = VerificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
