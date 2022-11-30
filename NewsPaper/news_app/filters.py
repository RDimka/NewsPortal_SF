import django_filters
from django_filters import FilterSet
from .models import Post
from django import forms


# Создаем свой набор фильтров для модели Post.
class PostFilter(FilterSet):
    title = django_filters.CharFilter(field_name='title',
                                      label='В названии:',
                                      lookup_expr='icontains', )
    author = django_filters.CharFilter(field_name='author__user__username',
                                       label='По автору:',
                                       lookup_expr='icontains', )
    date_time_in = django_filters.DateFilter(field_name='date_time_in',
                                             label='Начиная с даты:',
                                             widget=forms.DateInput(attrs={"type": "date"}),
                                             lookup_expr='date__gte', )
    # class Meta:
    # В Meta классе мы должны указать Django модель,
    # в которой будем фильтровать записи.
    # model = Post
    # В fields мы описываем по каким полям модели
    # будет производиться фильтрация.
    # fields = {
    # поиск по названию
    # 'title': ['icontains'],
    # количество товаров должно быть больше или равно
    # 'author__user__username': ['icontains'],
    # }
