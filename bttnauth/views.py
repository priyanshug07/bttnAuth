from rest_framework.decorators import api_view
from rest_framework.response import Response
from bttnauth.request_serializers.auth_request_serializers import *
from bttnauth.models import AuthTokens
import datetime
from bttnauth.utiils.generic_utils import check_token_sanity, get_new_auth_token
import logging


def generate_access_and_refresh_token(user_id):
    auth_token = AuthTokens()
    auth_token.user_id = user_id
    auth_token.access_token = get_new_auth_token()
    auth_token.refresh_token = get_new_auth_token()
    auth_token.auth_expires_at = datetime.datetime.now() + datetime.timedelta(days=7)
    auth_token.refresh_expires_at = datetime.datetime.now() + datetime.timedelta(days=30)
    auth_token.save()
    return auth_token

# this method is called post the success of OTP
@api_view(["POST"])
def get_access_token(request):
    user_id = request.data.get("user_id")
    data_validator = GenerateAuthRequestSerializer(data=request.data)
    if not data_validator.is_valid():
        return Response(data_validator.errors, status=400)

    try:
        auth_token = AuthTokens.objects.get(user_id=user_id)

    except AuthTokens.DoesNotExist:
        logging.info(f"Generating new token and refresh token for the user {user_id}")
        auth_token = generate_access_and_refresh_token(user_id)

    return Response(status=200, data={"user_id" : user_id, "auth_token": auth_token.access_token, "refresh_token": auth_token.refresh_token})

@api_view(["POST"])
def refresh_auth_token(request):
    user_id = request.data.get("user_id")
    validated_request = RefreshAuthTokenSerializer(data=request.data)
    validated_request.is_valid(raise_exception=True)
    if not validated_request.is_valid:
        return Response(validated_request.errors, status=400)

    AuthTokens.objects.filter(user_id=user_id).update(access_token=get_new_auth_token(), auth_expires_at=datetime.datetime.now() + datetime.timedelta(days =7))
    return Response(status=200, data={"user_id": user_id, "message": "token updated successfully"})

@api_view(["GET"])
def validate_token(request):
    access_token = request.headers.get("Authorization")
    if not access_token:
        return Response(status=400, data={"message": "access token not present in header"})
    try:
        auth_token = AuthTokens.objects.get(access_token=access_token)
    except AuthTokens.DoesNotExist:
        return Response(status=401, data={"message": "invalid access token provided"})
    if not check_token_sanity(auth_token.auth_expires_at):
        return Response(status=401, data={"message": "auth token has expired"})
    return Response(status=200, data={"message": "success", "user_id":  auth_token.user_id})

