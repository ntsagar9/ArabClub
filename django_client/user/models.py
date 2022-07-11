from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image


class Profile(models.Model):
    image = models.ImageField(default="default.png", upload_to="profile_pics")
    image_cover = models.ImageField(
        default="cover.jpg", upload_to="profile_cover"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} profile."

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        img_cover = Image.open(self.image_cover.path)
        if img.width > 450 or img.height > 450:
            img_size = (450, 450)
            img.thumbnail(img_size)
            img.save(self.image.path)

        elif (
            img_cover.width > 1250
            or img_cover.height > 450
            and img_cover.width < 1000
            or img_cover.height < 250
        ):
            img_cover.thumbnail((1250, 450))
            img_cover.save(self.image_cover.path)


def create_profile(sender, **kwarg):
    if kwarg["created"]:
        Profile.objects.create(user=kwarg["instance"])


post_save.connect(create_profile, sender=User)
