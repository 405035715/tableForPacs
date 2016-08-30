from django.conf.urls import url
from . import views

app_name = 'report'

urlpatterns = [
    url(r'^$', views.patientlistOfUS, name='patientlistOfUS'),
    url(r'patientlistOfUS', views.patientlistOfUS, name='patientlistOfUS'),
    url(r'reportOfUS/$', views.reportOfUS, name='reportOfUS'),
    url(r'patientlistOfFSK', views.patientlistOfFSK, name='patientlistOfFSK'),
    url(r'reportOfFSK/$', views.reportOfFSK, name='reportOfFSK'),
    url(r'patientlistOfENDO', views.patientlistOfENDO, name='patientlistOfENDO'),
    url(r'reportOfENDO/$', views.reportOfENDO, name='reportOfENDO'),
]