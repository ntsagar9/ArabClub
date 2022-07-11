import random

import django.db.utils
from django.contrib.auth import get_user_model

from newsfeed.models import FollowTags, Post, Tag
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
            "github_url": {
                "url": "https://www.github.com/user/",
                "user_id": user.pk,
            },
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
                "content": """
                Est lorem at dolore ipsum labore. Voluptua eos vel dolor magna
                et stet duo aliquyam dolore accumsan ipsum. Et sit vulputate
                sadipscing gubergren et et. Et consequat et ea. Rebum augue
                takimata sit ipsum hendrerit feugait aliquip dolor elitr tation
                adipiscing takimata. Cum et amet feugait nulla iriure eum.
                Hendrerit ipsum invidunt sadipscing tempor sit eleifend
                takimata. Amet velit volutpat erat duo dolore eum facilisis.
                """,
                "published_at": "2022-02-20T04:40:04.428433Z",
                "update_at": "2022-02-20T04:40:02Z",
                "user_id": user.pk,
            }
            post = Post.objects.create(**post_data)
            for tag in range(3):
                tag_data = {
                    "tag_name": tags_list[
                        random.randint(0, len(tags_list) - 1)
                    ],
                    "post_id": post.pk,
                }
                # print(tag_data)

                tags = Tag.objects.create(**tag_data)
                if tags.id is None:
                    tags = Tag.objects.get(tag_name=tag_data["tag_name"])

                # return print(tags.pk)
                follow_data = {"tags_id": tags.id, "user_id": user.pk}
                # return print(follow_data)
                FollowTags.objects.create(**follow_data)

        print(f"Create Done ID --> {user.id} username --> {user.username})")
        print("-" * 50)
