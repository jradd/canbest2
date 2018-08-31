from django.contrib import admin
from .models import Comment


# class CommentsAdmin(admin.ModelAdmin):
#     list_display = ("__str__", "timestamp", "post")
#     list_display_links = ("__str__", "post")
#     ordering = ("-timestamp", "-content")
#     list_filter = ("timestamp", )
#     search_fields = ("content", "user", "post")
#
#     class Meta:
#         model = Comment


admin.site.register(Comment)
