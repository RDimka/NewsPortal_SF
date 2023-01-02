from django.shortcuts import render
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from .forms import PostForm
from .filters import PostFilter

from django.contrib.auth.mixins import PermissionRequiredMixin

class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news_list'
    paginate_by = 10

    # Переопределяем функцию получения списка статей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict,
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'news.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news'


class PostSearchList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news_list'
    paginate_by = 10

    # Переопределяем функцию получения списка статей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict,
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

# Добавляем новое представление для редактирования постов.
class PostCreate(PermissionRequiredMixin, CreateView):

    permission_required = ('news_app.add_post',)

    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель постов
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        path = self.request.META['PATH_INFO']

        if path == '/newspaper/article/create/':  #если статья - ставим False. По умолчанию - новость - True
            post.is_news = False
        return super().form_valid(form)
class PostUpdate(PermissionRequiredMixin, UpdateView):

    permission_required = ('news_app.change_post',)

    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')