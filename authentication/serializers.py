from rest_framework import serializers
from .models import User, Buyer, Seller

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'date_joined', 'is_active']

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ['default_shipping_address', 'wishlist_items', 'preferred_categories', 'loyalty_points', 'is_verified_buyer']

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['store_name', 'business_registration_number', 'store_address', 'product_categories', 'is_verified_seller', 'total_sales']

class RegisterSerializer(serializers.ModelSerializer):
    buyer_profile = BuyerSerializer(required=False)
    seller_profile = SellerSerializer(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'buyer_profile', 'seller_profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        buyer_data = validated_data.pop('buyer_profile', None)
        seller_data = validated_data.pop('seller_profile', None)

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number')
        )

        if buyer_data:
            Buyer.objects.create(user=user, **buyer_data)
        if seller_data:
            Seller.objects.create(user=user, **seller_data)

        return user