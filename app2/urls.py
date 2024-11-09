from django.urls import path


from . import views

urlpatterns = [
    path("", views.CarCollectionView.as_view()),
    path("<int:pk>/", views.CarSingletonView.as_view())
]