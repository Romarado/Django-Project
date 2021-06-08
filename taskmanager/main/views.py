from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import RacerForm, AuthUserForm, RegisterUserForm, CommentForm, BugurtForm
from .models import Racer, Comments, Bugurt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
#В этом файле выполняются действия....


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return "%s?id=%s" % (self.success_url, self.object.id)


class NoteDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
    model = Bugurt
    template_name = "main/detail_view.html"
    context_object_name = 'note'
    form_class = CommentForm
    success_msg = 'Комментарий успешно создан! Ожитайте модерации'

    def get_success_url(self, **kwargs):
        return reverse_lazy('detail', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return HttpResponse('''
                   <div class="alert alert-success">
                           Ошибка!
                       </div>
                   ''')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.article = self.get_object()
        self.object.save()
        #super().form_valid(form)
        print('hello')
        #return render(request, template, context)
        #return JsonResponse({"text": 1}, status=200)
        #print(self.object)
        item = self.object
        print(item)
        template = 'main/comment_item.html'
        context = {'item': item, 'comment_msg': 'Комментарий опубликован!'}
        return render(self.request, template, context)


    # def form_invalid(self, form):
    #     """
    #     Если форма невалидна, возвращаем код 400 с ошибками.
    #     """
    #     super().form_invalid(form)
    #     errors = form.errors.as_json()
    #     return JsonResponse({"errors": errors}, status=400)


class RegisterUserView(CreateView):
    "Регистрация пользователя"
    model = User
    template_name = "main/register.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy('home')
    success_msg = "Вы успешно зарегестрировались!"

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class AuthUserView(LoginView):
    "Авторизация пользователя"
    template_name = "main/login.html"
    form_class = AuthUserForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('home')


def detail(request, pk):
    try:
        note = Racer.objects.get(id=pk)
    except:
        raise Http404("Запись не найдена!")
    return render(request, 'main/detail_view.html', {"note": note})


class UpdateRacerView(CustomSuccessMessageMixin, LoginRequiredMixin, UpdateView):
    "Обновление гонщика"
    model = Racer
    template_name = "main/form.html"
    form_class = RacerForm
    success_url = reverse_lazy('home')
    success_msg = 'Запись успешно обновлена!'
    context_object_name = 'key_form'
    login_url = 'login_page'

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print(kwargs['instance'].author)
        print(self.request.user)
        if kwargs['instance'].author != self.request.user\
                and kwargs['instance'].author != 'AnonymousUser':
            return self.handle_no_permission()
        return kwargs


class DeleteRacerView(LoginRequiredMixin, DeleteView):
    "Удаление гонщика"
    model = Racer
    template_name = 'main/form.html'
    success_url = reverse_lazy('home')
    success_msg = 'запись удалена'
    login_url = 'login_page'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


def index(request):
    print(request.user)
    values = Racer.objects.order_by('-id')
    return render(request, 'main/index.html', {"values": values})


class BugurtList(ListView):
    template_name = 'main/bugurt_list.html'
    context_object_name = 'values'
    model = Bugurt
    ordering = '-id'


def about(request):
    template = 'main/about.html'
    context = {
    }
    return render(request, template, context)


class CreateForm(CustomSuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login_page')
    model = Bugurt
    template_name = 'main/form.html'
    form_class = BugurtForm
    success_url = reverse_lazy('home')
    success_msg = 'Бугурт создан'

    def get_context_data(self, **kwargs):
        kwargs['values'] = Bugurt.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)
    #переопрeделeние метода для сохранения авторизованного пользователя как автора
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        print('beda')
        self.object.save()
        return super().form_valid(form)


def comment_form(request):
    form = CommentForm()
    if request.method == "POST" and request.is_ajax():
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            form.save()
            return JsonResponse({"text": text}, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)

    return render(request, "main/detail_view.html", {"note": form})


def update_comment_status(request, pk, type):
    "обновление статуса комментария"
    item = Comments.objects.get(pk=pk)
    if request.user != item.article.author:
        return HttpResponse('низя так')
    if type == 'publish':
        import operator
        item.status = operator.not_(item.status)
        item.save()
        template = 'main/comment_item.html'
        context = {'item': item, 'comment_msg': 'Комментарий опубликован!'}
        return render(request, template, context)
    elif type == 'delete':
        item.delete()
        return HttpResponse('''
        <div class="alert alert-success">
                Комментарий удален!
            </div>
        ''')
    return HttpResponse('1')

