"""python_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from articles import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from boards import views as board_views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin_url'),
    path('modify_articles/', views.mod_articles, name='modify_articles_url'),
    path('articles/<int:id_>/', views.article_view, name='article_url'),
    path('tags/<int:id_>/', views.tag_view, name='tag_url'),
    path('modify_tags/', views.mod_tags, name='modify_tags_url'),
    path('', views.home_view, name='home_url'),
    path('login/', auth_views.LoginView.as_view(), name='login_url'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_url'),
    path('signup/', account_views.signup, name='signup_url'),

    path('board/<int:id_>/', board_views.board_view, name='board_url'),

    path('post_reply/<int:id_>', board_views.reply_view, name='reply_url'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('reset_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('all_discussion_boards/', board_views.discussion_boards, name='boards'),
    path('summernote/', include('django_summernote.urls'))
]

# links media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

