from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import TodoItem
from .forms import TodoItemForm, SignUpForm

@login_required
def todo_list(request):
    todos = TodoItem.objects.filter(user=request.user)
    return render(request, 'todo/todo_list.html', {'todos': todos})

@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoItemForm()
    return render(request, 'todo/todo_form.html', {'form': form})

@login_required
def todo_update(request, pk):
    todo = TodoItem.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoItemForm(instance=todo)
    return render(request, 'todo/todo_form.html', {'form': form})

@login_required
def todo_delete(request, pk):
    todo = TodoItem.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todo/todo_confirm_delete.html', {'todo': todo})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todo_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
