from newsfeed.models import Post, FollowTags


class NewsFeed:
    def __init__(self):
        self.data = None
        self.tags = []

    def get_user_tags(self):
        user = self.request.user.pk
        self.tags = [tag.tags.tag_name for tag in
                     FollowTags.objects.filter(user_id=user)]

        self.data = (Post.objects.filter(post_tags__tag_name__in=self.tags))

        return self.data

    def get_feed(self):
        pass
