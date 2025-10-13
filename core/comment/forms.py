from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    rating = forms.ChoiceField(
        widget=forms.RadioSelect, choices=[(i, str(i)) for i in range(1, 6)]
    )

    class Meta:
        model = Comment
        fields = ["user", "book", "body", "name", "rating"]
