from django.db.models import Avg, Count
from django.http import JsonResponse
from django.views.generic.edit import BaseCreateView
from django.views.generic import ListView
from django.conf import settings

from .models import Comment
from .forms import CommentForm


class CommentListView(ListView):
    model = Comment
    template_name = "comment/comment.html"
    context_object_name = "comments"
    paginate_by = settings.COMMENTS_PER_PAGE

    def get_queryset(self):
        queryset = super().get_queryset()
        book_id = self.kwargs["book_id"]
        queryset = queryset.filter(book_id=book_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["average"] = float(
            self.get_queryset().aggregate(average=Avg("rating"))["average"]
        )
        return context


class CreateCommentView(BaseCreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.save()
        count_comments = (
            self.get_queryset()
            .filter(book_id=form.cleaned_data["book"])
            .aggregate(count=Count("id"))["count"]
        )
        return JsonResponse(
            {"status": 200, "message": "Comment saved", "count": count_comments}
        )

    def form_invalid(self, form):
        response_errors = {}
        for field, e in form.errors.as_data().items():
            response_errors[field] = [str(t)[2:-3] for t in e]
        return JsonResponse(
            {"status": 204, "message": "Comment don`t save", "errors": response_errors}
        )
