from rest_framework import generics
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def home(request):
     html_content = """
    <html>
    <head>
        <title>Backend server for Super Ray</title>
    </head>
    <body>
        <h1>Backend server for Super Ray is running!!</h1>
        <ul>
            <li><a href="/admin">/admin</a></li>
            <li><a href="/api/super-resolution">api for super resolution</a></li>
            <li><a href="/api/token">api for login</a></li>
            <li><a href="/api/token/refresh">api for token refresh</a></li>
            <li><a href="/api/register">api for register</a></li>
            <li><a href="/api/logout">api for logout</a></li>
            <li><a href="/api/profile">api for to view profile</a></li>
            <li><a href="/api/profile/update">api for update profile</a></li>
    </body>
    </html>
    """
     return HttpResponse(html_content) 

  


