# notes/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Notes(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    title = models.CharField(max_length=200)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    tags = models.ManyToManyField(Tag, blank=True)
    is_completed = models.BooleanField(default=False)

    def is_overdue(self):
        if self.due_date and not self.is_completed:
            return timezone.now() > self.due_date
        return False

    class Meta:
        ordering = ['due_date', '-priority', '-created']

# notes/forms.py
from django import forms
from .models import Notes, Tag

class NotesForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )

    class Meta:
        model = Notes
        fields = ('title', 'text', 'tags', 'due_date', 'priority')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-5'}),
            'text': forms.Textarea(attrs={"class": "form-control mb-5"}),
            'priority': forms.Select(attrs={"class": "form-control mb-3"})
        }
        labels = {
            'text': 'Write your thoughts here:',
            'due_date': 'When do you need this done?',
            'priority': 'How important is this?'
        }

# notes/views.py
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes/notes_list.html"
    login_url = "/login"

    def get_queryset(self):
        queryset = self.request.user.notes.all()

        # Filter by tags
        tags = self.request.GET.getlist('tag')
        if tags:
            queryset = queryset.filter(tags__name__in=tags).distinct()

        # Filter by status
        status = self.request.GET.get('status')
        if status == 'completed':
            queryset = queryset.filter(is_completed=True)
        elif status == 'pending':
            queryset = queryset.filter(is_completed=False)
        elif status == 'overdue':
            queryset = queryset.filter(
                due_date__lt=timezone.now(),
                is_completed=False
            )

        # Filter by priority
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['selected_tags'] = self.request.GET.getlist('tag')
        context['current_filters'] = {
            'status': self.request.GET.get('status', ''),
            'priority': self.request.GET.get('priority', '')
        }
        return context