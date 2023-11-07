from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.start, name="start"),
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('chathome',views.chathome,name="chathome"),
    path('profile',views.profile, name ="profile"),
    path('chathistory', views.chathistory, name ="chathistory"),
    path('store-message-endpoint', views.store_message, name='store_message'),
    path('authentication/getResponse',views.getResponse,name='getResponse')
]
