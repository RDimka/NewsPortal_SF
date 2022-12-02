from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostSearchList, PostCreate, PostUpdate, PostDelete


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем статьям у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name='news_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(), name='news_detail'),
   path('search', PostSearchList.as_view(), name='news_search'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update', PostUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
]