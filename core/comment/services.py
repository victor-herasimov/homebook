from django.db.models import Avg, Count, QuerySet
from core.abstract.services import AbstractService
from core.comment.models import Comment


class CommentService(AbstractService):
    model = Comment

    def get_comments_by_book_id(self, book_id: int) -> QuerySet:
        return self.model.objects.select_related("user", "book").filter(book_id=book_id)

    def get_count_for_book(self, book_id) -> int:
        return (
            self.get_all().filter(book_id=book_id).aggregate(count=Count("id"))["count"]
        )

    def get_average_rating(self, queryset) -> float:
        return float(queryset.aggregate(average=Avg("rating"))["average"])
