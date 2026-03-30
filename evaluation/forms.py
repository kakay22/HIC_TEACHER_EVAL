from django import forms
from .models import Section, Question, Course

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['prefix', 'title']
        widgets = {
            'prefix': forms.TextInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Section Prefix'}),
            'title': forms.TextInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Section Title'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'order']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Question Text'}),
            'order': forms.NumberInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Order'}),
            'section': forms.HiddenInput(),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'code': forms.TextInput(attrs={'class': 'w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }
