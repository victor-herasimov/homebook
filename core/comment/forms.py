from django import forms

from core.comment.services import CommentService


class CommentForm(forms.ModelForm):
    rating = forms.ChoiceField(
        widget=forms.RadioSelect, choices=[(i, str(i)) for i in range(1, 6)]
    )

    class Meta:
        model = CommentService().get_model()
        fields = ["user", "book", "body", "name", "rating"]
