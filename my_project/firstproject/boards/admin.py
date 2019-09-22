from django.contrib import admin
from .models import Board,Post,Topic
# Register your models here.
class Topic_date(admin.ModelAdmin):
    list_display = [ "subject","created_by","created_dt"]
    class Meta:
        model = Topic
class Post_sitt(admin.ModelAdmin):
    list_display = ["message","created_by"]
    class Meta:
        model = Post

admin.site.register(Board)
admin.site.register(Post,Post_sitt)
admin.site.register(Topic,Topic_date)
