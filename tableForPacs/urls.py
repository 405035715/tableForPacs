from django.conf.urls import url,include
from django.contrib import admin
import tablespacs

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tablespacs/', include('tablespacs.urls')),   #放射统计
    url(r'^report/', include('report.urls')),   #报告
    url(r'^videocapture/', include('tjVideoCapture.urls')),   #b超统计
]
