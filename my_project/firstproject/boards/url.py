from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('boards/<int:id>/',views.TopicListView.as_view(), name="boards_topic"),
    path('boards/<int:id>/new_topic/',views.new_topic, name="new_topic"),
    path('boards/<int:id>/topics/<int:topic_id>/', views.PostListView.as_view(), name='topic_posts'),
    path('boards/<int:id>/topics/<int:topic_id>/replay/', views.replay_topic, name='replay_topic'),
    path('boards/<int:id>/topics/<int:topic_pk>/posts/<int:post_pk>/deletePost/', views.DeletePost.as_view(), name='deletePost'),
    path('boards/<int:id>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('boards/<int:id>/topics/<int:topic_pk>/posts/<int:post_pk>/like/', views.LikesPosts.as_view(), name='like-toggl')
]
