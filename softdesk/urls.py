"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from softdesk.accounts.views import SoftUserViewSet, ContributorViewSet
from softdesk.projects.views import ProjectViewSet, IssueViewSet, CommentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r"users", SoftUserViewSet)
router.register(r"contributors", ContributorViewSet)
router.register(r"projects", ProjectViewSet)
router.register(r"issues", IssueViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls
