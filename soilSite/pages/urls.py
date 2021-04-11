from django.urls import path
from .views import (
    home_view,
    loam_view,
    silt_view,
    clay_view,
    loam_view2,
    silt_view2,
    clay_view2,
)


urlpatterns = [
    path('home/', home_view, name="home"),
    path('loam-soil/<str:comp>', loam_view, name="loam"),
    path('silt-soil/<str:comp>', silt_view, name="silt"),
    path('clay-soil/<str:comp>', clay_view, name="clay"),
    path('loam-soil/', loam_view2, name="loam2"),
    path('silt-soil/', silt_view2, name="silt2"),
    path('clay-soil/', clay_view2, name="clay2"),
]

