from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.utils import timezone
from django.urls import reverse  # Changed from django.utils to django.urls
from django.shortcuts import get_object_or_404, redirect
from .models import Notes, Tag
from .forms import NotesForm

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes/notes_list.html"
    login_url = "/login"

    def get_queryset(self):
        queryset = self.request.user.notes.all()

        # Filter by tags
        tags = self.request.GET.getlist('tags')
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
        context['available_tags'] = Tag.objects.filter(
            notes__user=self.request.user
        ).annotate(
            notes_count=Count('notes')
        ).distinct()
        
        context['selected_tags'] = self.request.GET.getlist('tags')
        context['current_filters'] = {
            'status': self.request.GET.get('status', ''),
            'priority': self.request.GET.get('priority', '')
        }
        return context

class NotesDetailView(LoginRequiredMixin, DetailView):
    model = Notes
    context_object_name = "note"
    login_url = "/login"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class NotesCreateView(LoginRequiredMixin, CreateView):
    model = Notes
    success_url = '/smart/notes'
    form_class = NotesForm
    login_url = "/login"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NotesUpdateView(LoginRequiredMixin, UpdateView):
    model = Notes
    success_url = '/smart/notes'
    form_class = NotesForm
    login_url = "/login"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class NotesDeleteView(LoginRequiredMixin, DeleteView):
    model = Notes
    success_url = '/smart/notes'
    template_name = 'notes/notes_delete.html'
    login_url = "/login"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class NotesToggleCompleteView(LoginRequiredMixin, View):
    login_url = "/login"

    def post(self, request, pk):
        note = get_object_or_404(Notes, pk=pk, user=request.user)
        note.is_completed = not note.is_completed
        note.save()
        return redirect('notes.detail', pk=pk)
    model = Notes
    success_url = '/smart/notes'
    template_name = 'notes/notes_delete.html'
    login_url = "/login"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)