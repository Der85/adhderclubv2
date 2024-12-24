# forms.py
from django import forms
from .models import Notes, Tag

class NotesForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags (comma separated)'
        })
    )

    class Meta:
        model = Notes
        fields = ('title', 'text', 'due_date', 'priority')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-5'}),
            'text': forms.Textarea(attrs={"class": "form-control mb-5"}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'priority': forms.Select(attrs={'class': 'form-control mb-3'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['tags'] = ', '.join(tag.name for tag in self.instance.tags.all())

    def save(self, commit=True):
        note = super().save(commit=False)
        
        if self.user and not note.pk:  # Only set user for new notes
            note.user = self.user
        
        if commit:
            note.save()
            
            # Handle tags
            if 'tags' in self.cleaned_data:
                tag_names = [name.strip() for name in self.cleaned_data['tags'].split(',') if name.strip()]
                
                # Clear existing tags
                note.tags.clear()
                
                # Create or get tags and add them to the note
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        user=note.user,  # Use note.user instead of self.user
                        defaults={'user': note.user}  # Provide default value for user
                    )
                    note.tags.add(tag)
                    
        return note