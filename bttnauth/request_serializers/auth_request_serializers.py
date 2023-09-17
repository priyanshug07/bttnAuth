from rest_framework import serializers
from bttnauth.models import AuthTokens
from bttnauth.utiils.generic_utils import check_token_sanity


class GenerateAuthRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)

class RefreshAuthTokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    refresh_token = serializers.CharField(required=True)

    def validate(self, data):
        try:
            auth_token = AuthTokens.objects.get(user_id = data.get("user_id"), refresh_token= data.get("refresh_token"))
        except AuthTokens.DoesNotExist:
            raise serializers.ValidationError("No auth token entry found for user")

        if not check_token_sanity(auth_token.refresh_expires_at):
            raise serializers.ValidationError("Refresh token has expired")
        return data
