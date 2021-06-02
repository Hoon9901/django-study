from django.urls import path
from mega import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mega'   # 네임스페이스 추가

urlpatterns = [
    # base_views
    path('', views.index, name = 'index'),  # /mega/ -> index
    path('team1/', views.team1, name = 'team1'),
    path('team2/', views.team2, name = 'team2'),
    path('team3/', views.team3, name = 'team3'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

