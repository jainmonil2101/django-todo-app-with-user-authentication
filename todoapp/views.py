from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        search_query = request.GET.get('search_query') or ''

        search_result = Task.objects.filter(
            user=request.user, title__startswith=search_query)
        task_count = Task.objects.filter(
            user=request.user, complete=False).count()
        params = {
            'search_result': search_result,
            'search_query': search_query,
            'task_count': task_count,

        }
        return render(request, 'home.html', params)
    else:
        return redirect('login')


def register(request):
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    if request.method == 'POST':
        try:
            if password1 == password2:
                user = User.objects.create_user(
                    username=username, password=password1)
                user.save()
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'register.html', {'form': UserCreationForm(), 'error': "Passwords didn't match!"})
        except IntegrityError:
            return render(request, 'register.html', {'form': UserCreationForm(), 'error': "Username already exists. Please choose a different username!"})
    else:
        return render(request, 'register.html', {'form': UserCreationForm()})


def logout_user(request):
    logout(request)
    return redirect('login')


def login_user(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'form': AuthenticationForm(), 'error': "Username or Password didn't match. Please try again!"})
    else:
        return render(request, 'login.html', {'form': AuthenticationForm()})


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'task_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'task_form.html'
    success_url = reverse_lazy('home')


@login_required
def deletetask(request, task_pk):
    task = get_object_or_404(Task, user=request.user, pk=task_pk)
    task.delete()
    return redirect('home')


@login_required
def complete(request, task_pk):
    task_complete = get_object_or_404(
        Task, user=request.user, complete=False, id=task_pk)
    task_complete.complete = True
    task_complete.save()
    return redirect('home')


@login_required
def incomplete(request, task_pk):
    task_incomplete = get_object_or_404(
        Task, user=request.user, complete=True, id=task_pk)
    task_incomplete.complete = False
    task_incomplete.save()
    return redirect('home')
