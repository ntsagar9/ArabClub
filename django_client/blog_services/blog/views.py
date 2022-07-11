from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import NewComment, PostCreateView, PostUpdateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormView


def landing_page(request):
    return render(request, "blog/landing_page.html")


def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)
    context = {
        "title": "الصفحة الرئسية",
        "posts": posts,
        "page": page,
    }
    return render(request, "blog/index.html", context)


def about(request):
    return render(request, "blog/about.html", {"title": "من نحن؟"})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    comments = post.comments.filter(active=True)

    if request.method == "POST":

        comment_form = NewComment(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = NewComment()

    context = {
        "title": post,
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
    }

    return render(request, "blog/detail.html", context)


class PostCreateView(FormView):
    template_name = "blog/new_post.html"
    form_class = PostCreateView

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     template_name = "blog/new_post.html"
#     form_class = PostCreateView
#
#     def get(self, request, *args, **kwargs):
#         print(request.user)
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_update.html"
    form_class = PostUpdateView

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
