import random

import django.db.utils
from django.contrib.auth import get_user_model

from newsfeed.models import Post, Tag, FollowTags
from users.serializers import UserSerializer

model = get_user_model()

tags_list = [
    "python",
    "djagno",
    "javaScript",
    "C",
    "C++",
    "C#",
    "Haskl",
    "Pascal",
    "Rust",
    "Rube",
    "Go",
    "Scala",
]


def create_user():
    for i in range(2, 1000000):
        data = {
            "username": f"test_user_{i}",
            "email": f"test@mail{i}.com",
            "date_of_birth": "1999-7-13",
            "password": "123",
        }
        try:
            user = model.objects.create_user(**data)
        except django.db.utils.IntegrityError:
            continue
        update = {
            "name": {
                "first_name": f"test_user_{i}",
                "last_name": f"Kamel{i}",
                "user_id": user.pk,
            },
            "bio": {"bio": "hello Friend", "user_id": user.pk},
            "skills": {"skill_name": "Python, docker, c", "user_id": user.pk},
            "github_url": {"url": "https://www.github.com/user/", "user_id": user.pk},
            "phone": {"phone": "01066373279", "user_id": user.pk},
            "address": {
                "country": "Egypt",
                "city": "Qena",
                "street_name": "Qus",
                "user_id": user.pk,
            },
        }
        serializer = UserSerializer(data=update)
        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
        for post in range(10):
            post_data = {
                "title": f"Post Number {i}",
                "content": "Est lorem at dolore ipsum labore. Voluptua eos vel dolor magna et stet duo aliquyam dolore accumsan ipsum. Et sit vulputate sadipscing gubergren et et. Et consequat et ea. Rebum augue takimata sit ipsum hendrerit feugait aliquip dolor elitr tation adipiscing takimata. Cum et amet feugait nulla iriure eum. Hendrerit ipsum invidunt sadipscing tempor sit eleifend takimata. Amet velit volutpat erat duo dolore eum facilisis. Sed amet at lobortis rebum nonummy ipsum commodo tempor zzril sanctus elitr consequat et consequat. Tempor diam feugiat ipsum ipsum rebum sit diam kasd. Gubergren tation dolore ut qui diam amet vel nobis magna doming vero dolores no nonumy. No ut ut accumsan stet tempor vel. Adipiscing ut ea vero sit ea lorem ut consetetur dolor luptatum quis et duo clita kasd aliquyam elitr.\r\n\r\nEt congue sadipscing qui luptatum elit est ea accusam tempor vel at eros. Erat aliquam voluptua. Vel lorem et kasd stet vel. Consetetur et elitr vero eirmod sed nisl dolores elitr kasd et elitr rebum elitr in. Et sed velit nonumy sed ipsum feugiat rebum kasd sed no ad amet elitr vulputate vel at elitr diam. Stet elitr dolor diam voluptua sea ipsum diam dolor diam facilisis commodo sanctus nibh enim. Vero consetetur tempor sed sit kasd eum ipsum justo. Duo sit nonumy. Adipiscing eos dolor dolore ipsum facer voluptua nihil duis dolores blandit aliquip ullamcorper.\r\n\r\nKasd tation placerat suscipit sea kasd sit est lorem. Ipsum dolor lorem sed invidunt possim ipsum nam sanctus amet tation imperdiet takimata. Diam odio iriure ex ipsum et rebum invidunt clita magna no ipsum amet.\r\n\r\nEst dolor sit dolor eirmod amet vel et accusam hendrerit dolor amet consetetur. Nonumy eirmod labore duo clita adipiscing stet ea ut ipsum sed magna et ea. Et ullamcorper erat elitr at sit ipsum ut in justo duo commodo dolore aliquyam et. In justo dolore lobortis et in dolore lorem erat kasd diam clita ipsum et sea sed voluptua ipsum sea. Justo exerci qui invidunt et ex vulputate ipsum kasd aliquyam erat vel sit sit odio. Ut iriure et et voluptua sit stet ea sea. Eos labore kasd et. Iriure dolore velit eirmod dolore zzril amet dolores dolore duo adipiscing labore. Takimata quis vel. Lorem stet sadipscing congue et. Erat et id velit in nonumy tincidunt sanctus esse magna et. Dolor gubergren no esse.\r\n\r\nRebum tempor odio ad takimata stet laoreet eu ea et aliquyam ipsum erat sed kasd nulla. Et sanctus kasd stet diam nonumy stet no eu doming wisi sit in consetetur lorem. Lorem ea amet vel luptatum et nulla stet clita accusam iusto at vulputate autem id. Volutpat molestie elitr sit justo dolor dolore duis nulla qui gubergren tempor kasd magna nonummy diam duis.\r\n\r\nVero ea dolore euismod amet at dolor takimata sanctus ex tempor et. Dolor ut labore eirmod sit ipsum commodo sit dolore magna nonumy sit sanctus consetetur ipsum aliquyam dolore. Consetetur at invidunt et lorem sit stet sadipscing euismod. Nostrud dolore gubergren ut adipiscing eos invidunt gubergren. Nonumy takimata praesent invidunt nulla iriure cum consetetur diam consetetur luptatum sed feugiat rebum. Eros consetetur dolor ut invidunt. Voluptua nulla elitr diam eos dolore stet sit erat et elitr sadipscing erat.",
                "published_at": "2022-02-20T04:40:04.428433Z",
                "update_at": "2022-02-20T04:40:02Z",
                "user_id": user.pk,
            }
            post = Post.objects.create(**post_data)
            for tag in range(3):
                tag_data = {
                    "tag_name": tags_list[random.randint(0, len(tags_list) - 1)],
                    "post_id": post.pk,
                }
                # print(tag_data)

                tags = Tag.objects.create(**tag_data)
                if tags.id is None:
                    tags = Tag.objects.get(tag_name=tag_data["tag_name"])

                # return print(tags.pk)
                follow_data = {"tags_id": tags.id, "user_id": user.pk}
                # return print(follow_data)
                follow = FollowTags.objects.create(**follow_data)

        print(f"Create Done ID --> {user.id} username --> {user.username})")
        print("-" * 50)
