from rest_framework import generics
from .serializers import RegisterSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .models import Family
from .serializers import FamilySerializer, FamilyMemberSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "fname": user.fname,
        "lname": user.lname,
        "mobile": user.mobile,
        "email": user.email,
        "family": user.family.id if user.family else None
    })

class CreateFamilyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.family:
            return Response(
                {"error": "You already belong to a family"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = FamilySerializer(data=request.data)

        if serializer.is_valid():
            family = serializer.save(created_by=user)

            # Assign creator to family
            user.family = family
            user.save()

            return Response(
                FamilySerializer(family).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class JoinFamilyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        code = request.data.get("code")

        if user.family:
            return Response(
                {"error": "You already belong to a family"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            family = Family.objects.get(code=code)
        except Family.DoesNotExist:
            return Response(
                {"error": "Invalid family code"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.family = family
        user.save()

        return Response(
            {"message": "Joined family successfully"},
            status=status.HTTP_200_OK
        )    

class MyFamilyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.family:
            return Response(
                {"message": "User does not belong to any family"},
                status=status.HTTP_200_OK
            )

        serializer = FamilySerializer(user.family)
        return Response(serializer.data)

class FamilyMembersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.family:
            return Response(
                {"error": "You are not part of any family"},
                status=status.HTTP_400_BAD_REQUEST
            )

        members = user.family.members.all()
        serializer = FamilyMemberSerializer(members, many=True)

        return Response(serializer.data)        
