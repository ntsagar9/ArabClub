from newsfeed.models import Post, FollowTags
from .pagination import post_queue


class NewsFeed:
    @property
    def data(self):
        return self._data

    def __init__(self):
        self.data = None
        self.tags = []

    def get_user_tags(self, post_count=100):
        user = self.request.user.pk
        if user is not None:
            self.tags = [
                tag.tags.tag_name for tag in FollowTags.objects.filter(user_id=user)
            ]
            if len(self.tags):
                self.data = Post.objects.filter(post_tags__tag_name__in=self.tags)[0:post_count]
                return self.data
        return self.get_feed()

    def get_feed(self):
        """
        Get just 10 post in reqeust become from None
        """
        self.data = Post.objects.all()[0:10]
        return self.data

    @data.setter
    def data(self, value):
        self._data = value
