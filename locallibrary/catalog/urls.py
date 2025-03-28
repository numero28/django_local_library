from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.book, name='book'),
    path('book/<int:pk>', views.book_detail, name='book_detail'),
    path('author/', views.author, name='author'),
    path('author/<int:pk>', views.author_detail, name='author_detail'),
    path('accounts/login', views.login, name='login'),
    path('accounts/logout', views.logout, name='logout'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBooksByLibrarianListView.as_view(),
         name='borrowed'),
    path('form/', views.form, name='form'),
    path('form/<str:name>', views.form_detail, name='form_detail'),    
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]
