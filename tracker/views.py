from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import Project, Task, User
from .forms import ProjectForm, TaskForm, TaskFilterForm
from django.utils import timezone

# Dashboard
def dashboard(request):
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    tasks_by_status = Task.objects.values('status').annotate(count=Count('id'))
    overdue_tasks = Task.objects.filter(due_date__lt=timezone.now(), status__in=['todo', 'inprogress']).count()

    context = {
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'tasks_by_status': tasks_by_status,
        'overdue_tasks': overdue_tasks,
    }
    return render(request, 'tracker/dashboard.html', context)

# Projects
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tracker/project_list.html', {'projects': projects})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'tracker/project_form.html', {'form': form})

def project_archive(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.status = 'archived'
    project.save()
    return redirect('project_list')

# Tasks
def task_list(request):
    tasks = Task.objects.all()
    form = TaskFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['user']:
            tasks = tasks.filter(assigned_to__name__icontains=form.cleaned_data['user'])
        if form.cleaned_data['priority']:
            tasks = tasks.filter(priority=form.cleaned_data['priority'])
        if form.cleaned_data['due_date']:
            tasks = tasks.filter(due_date=form.cleaned_data['due_date'])

    return render(request, 'tracker/task_list.html', {'tasks': tasks, 'form': form})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tracker/task_form.html', {'form': form})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('task_list')
    return render(request, 'tracker/task_form.html', {'form': form})
