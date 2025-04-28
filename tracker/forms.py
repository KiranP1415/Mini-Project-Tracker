from django import forms
from .models import Project, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'assigned_to', 'due_date', 'priority', 'status']

class TaskFilterForm(forms.Form):
    user = forms.CharField(required=False)
    priority = forms.ChoiceField(choices=[('', 'All')] + Task.PRIORITY_CHOICES, required=False)
    due_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
