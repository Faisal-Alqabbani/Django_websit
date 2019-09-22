from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse,Http404
from .models import Board,Topic,Post
from django.contrib.auth.models import User
from .forms import NewTopicForm,Postform
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,UpdateView,DeleteView,RedirectView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from django.urls import reverse_lazy

# Create your views here.

def index(request):
    boards = Board.objects.all()
    # Board_name = list()
    # for board in boards:
    #    Board_name.append(board.name)
    # res_respons = '<br>'.join(Board_name)
    # return HttpResponse(res_respons)
    return render(request,'home.html',{'boards':boards})

def boards_topic(request, id):
    board = get_object_or_404(Board, pk=id)
    queryset = board.topics.order_by('-created_dt').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 20)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)

    return render(request, 'topics.html', {'board': board, 'topics': topics})

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('id'))
        queryset = self.board.topics.order_by('-created_dt').annotate(replies=Count('posts') - 1)
        return queryset


@login_required()
def new_topic(request,id):
    board = get_object_or_404(Board, pk=id)
    user = request.user
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user)
        # subject = request.POST['subject']
        # message = request.POST['message']
        # if you want check in the terminal :print(subject,message)

        # topic = Topic.objects.create(subject=subject, created_by=user, board=board)

            return redirect('boards_topic', board.pk)
    form = NewTopicForm()
    return render(request,'new_topic.html', {'board': board, 'form': form})
def topic_posts(request,id,topic_id):
    topic = get_object_or_404(Topic,board__pk=id, pk=topic_id)
    topic.views += 1
    topic.save()
    queryset = topic.posts.order_by('-created_dt').annotate(replies=Count('topic') - 1)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 2)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)

    return render(request,'topic_posts.html', {'topic': topic, 'topics': topics})

@login_required()
def replay_topic(request,id,topic_id):
    topic = get_object_or_404(Topic, board__pk=id, pk=topic_id)
    if request.method == 'POST':
        form = Postform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            #post.message = form.clean_dd()
            post.save()

            return redirect('topic_posts', id=id, topic_id=topic.pk)
    else:
        form = Postform()

    return render(request, 'replay_topic.html', {'topic': topic, 'form': form})

@method_decorator(login_required,name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by = self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', id=post.topic.board.pk, topic_id=post.topic.pk)


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('id'), pk=self.kwargs.get('topic_id'))
        queryset = self.topic.posts.order_by('created_dt')
        return queryset

class DeletePost(DeleteView):
    model = Post
    fields = ('message',)
    template_name = 'DeletePost.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'
    success_url = '/'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)
class LikesPosts(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post , board__pk= self.kwargs.get('id'), topic_pk=self.kwargs.get('topic_pk'), pk=self.pk)
        user = self.request.user
        if user.is_authenticated:
            if user in post.likes.all():
                post.likes.remove(user)
            else:
                post.likes.add(user)
        return post.get_absolute_url()
