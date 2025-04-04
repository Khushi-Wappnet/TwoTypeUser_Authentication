from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Buyer, Seller
from .serializers import RegisterSerializer, UserSerializer, BuyerSerializer, SellerSerializer
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        buyer_profile = request.data.get('buyer_profile')
        seller_profile = request.data.get('seller_profile')

        # Check if the user already exists
        from .models import User
        try:
            user = User.objects.get(email=email)
            # If the user exists, check if they want to register as a seller
            if seller_profile:
                if hasattr(user, 'seller_profiles') and user.seller_profiles.exists():
                    return Response({"error": "User is already registered as a seller."}, status=status.HTTP_400_BAD_REQUEST)
                Seller.objects.create(user=user, **seller_profile)
                return Response({"message": "Seller profile added successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "User already exists. Provide seller profile to register as a seller."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # If the user does not exist, create a new user
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            user_roles = []
            if user.buyer_profiles.exists():
                user_roles.append('buyer')
            if user.seller_profiles.exists():
                user_roles.append('seller')

            return Response({
                "token": token.key,
                "roles": user_roles,
                "email": user.email
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)

        buyer_profiles = BuyerSerializer(user.buyer_profiles.all(), many=True).data
        seller_profiles = SellerSerializer(user.seller_profiles.all(), many=True).data

        return Response({
            "user": user_serializer.data,
            "buyer_profiles": buyer_profiles,
            "seller_profiles": seller_profiles
        })