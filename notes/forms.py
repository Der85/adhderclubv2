from django import forms
from .models import Notes, Tag

class NotesForm(forms.ModelForm):
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control my-5'}))

    class Meta:
        model = Notes
        fields = ('title', 'text', 'due_date', 'tags')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-5'}),
            'text': forms.Textarea(attrs={"class": "form-control mb-5"}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'text': 'Write your thoughts here:',
            'due_date': 'Due Date:',
            'tags': 'Tags (comma-separated):',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        tags = self.cleaned_data['tags']
        if commit:
            instance.save()
            # Handle tag creation
            if tags:
                tag_names = [tag.strip() for tag in tags.split(',')]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name, user=instance.user)
                    instance.tags.add(tag)
        return instance