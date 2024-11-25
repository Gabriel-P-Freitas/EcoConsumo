from flask import Blueprint
from extensions import oauth

google = oauth.register(
    name='google',
    client_id="463383199138-ua2bpp0et6eiap77vnd82t9hj12qqmim.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

