from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

# use app_name as namespace
app_name = 'FeQta'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name="home"),
    path('topics/', views.TopicListView.as_view(), name="topic_list"),
    path('topics/<slug>/', views.TopicDetailView.as_view(), name="topic_detail"),
    path('topic-follow/<slug>', views.TopicFollowToggle, name="topic_follow"),
    path('ask/', views.QuestionCreateView.as_view(), name="question_create"),
    path('question/<slug>/', views.QuestionDetailView.as_view(), name="question_detail"),
    path('question-follow/<slug>', views.QuestionFollowToggle, name="question_follow"),
    path('question/answer-new/<slug>/', views.AnswerCreateView.as_view(), name="answer_create"),
    path('answer/<slug>/', views.AnswerDetailView.as_view(), name="answer_detail"),
    path('answer/<slug>/edit/', views.AnswerUpdateView.as_view(), name="answer_update"),
    path('answer/<slug>/delete/', views.AnswerDeleteView.as_view(), name="answer_delete"),
    path('answer-delete/<slug>', views.AnswerDeletePage.as_view(), name="answer_delete_page"),
    path('delete-success/', views.AnswerDeleteSuccess.as_view(), name="delete_success"),
    path('answer-like/<slug>', views.LikeToggle, name="answer_like"),
    path('answer-needs-improvement/<slug>', views.NeedimpToggle, name="answer_need_imp"),
    path('answer-dislike/<slug>', views.DislikeToggle, name="answer_dislike"),
    path('answers/', views.AnswersView.as_view(), name="answers"),
    path('search/', views.SearchListView.as_view(), name="search"),
    path('profile/<username>/', views.ProfileDetailView.as_view(), name="profile_detail"),
    path('profile-follow/', views.ProfileFollowToggle.as_view(), name="profile_follow"),
    path('ranks/', views.RanksView.as_view(), name="ranks"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView, name="logout"),
    path('logout-page/', views.LogoutPage.as_view(), name="logout_page"),
    path('get-started/', views.RegisterView.as_view(), name="register")
]

# path('topics/<slug1>/<slug2>/',views.QuestionDetailView.as_view(), name="question_detail"),
