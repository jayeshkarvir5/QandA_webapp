"""QandA_webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from FeQta import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.HomeView.as_view(), name="home"),
    path('topics/', views.TopicListView.as_view(), name="topics"),
    path('topics/<slug>/', views.TopicDetailView.as_view(), name="topic_detail"),
    path('add-topic/', views.TopicCreateView.as_view(), name="topic_create"),
    path('answers/', views.AnswersView.as_view(), name="answers"),
    path('ranks/', views.RanksView.as_view(), name="ranks"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('get-started/', views.GetStartedView.as_view(), name="get_started"),
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
