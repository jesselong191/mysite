'''
app 路由文件
'''
from django.urls import  path
from . import  views
#定义URL命名空间
app_name ='polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # /polls/5(id)
    path('/<int:pk>/', views.DetailView.as_view(), name='detail'),
    # /polls/5/result
    path('/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('/<int:question_id>/vote/', views.vote, name='vote'),
]