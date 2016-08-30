from django.conf.urls import url
from . import views


app_name = 'polls'

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
       # ex: /polls/5/
    url(r'^[0-9]{1}/$', views.testjQuery, name='testjQuery'),
    url(r'^grid/$',views.grid, name='grid'),
    url(r'^grid_data/$',views.grid_data, name='grid_data'),
    url(r'^ajax/$',views.ajax, name='ajax'),
    url(r'^bodypartDic/$',views.bodypartDic, name='bodypartDic'),
]