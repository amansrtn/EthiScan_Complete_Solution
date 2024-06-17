from django.urls import path

from . import views

urlpatterns = [
    path('show/', views.statistics_view, name="show"),
    path('getWebName/', views.getMonths, name="get-webName"),
    path('getYear/', views.getYear, name="get-year"),
    path("webvscount/<str:webName>/", views.get_web_vs_count, name="Web-Vs-Count"),
    path("ctgrydist/", views.categoryDist, name="Category-Distribution"),
    path("mnthdist/<int:year>/", views.monthDist, name="month-distribution"),
    path("webvsmnth/<int:year>/<str:webName>/", views.get_monthly_counts_for_website, name="site-month")
]