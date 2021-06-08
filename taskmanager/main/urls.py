from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('bugurts/', views.BugurtList.as_view(), name='bugurt'),
    path('join-us/', views.CreateForm.as_view(), name='form'),
    path('about', views.about, name='about'),
    path('notes/<int:pk>/', views.NoteDetailView.as_view(), name='detail'),
    path('notes/<int:pk>/update/', views.UpdateRacerView.as_view(), name='update'),
    path('notes/<int:pk>/delete/', views.DeleteRacerView.as_view(), name='delete'),
    path('login/', views.AuthUserView.as_view(), name='login_page'),
    path('register/', views.RegisterUserView.as_view(), name='register_page'),
    path('logout/', views.LogoutUserView.as_view(), name='logout_page'),

    #ajax
    path('update_comment_status/<int:pk>/<slug:type>', views.update_comment_status, name='update_comment_status'),
  #  path('comment_form/', views.comment_form, name='comment_form')
]