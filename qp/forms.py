# forms.py
from django import forms

class QuestionPaperForm(forms.Form):
    Topic = forms.CharField(max_length=100, required=True, label="Topic")
    Sub_Topic = forms.CharField(max_length=100, required=True, label="Sub-Topic")
    Level = forms.ChoiceField(
        choices=[('Easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        required=True,
        label="Difficul Level"
    )
    number_of_questions = forms.IntegerField(min_value=1, required=True, label="Number of Questions")
