from django.contrib.auth import get_user_model
from Imstagram.models import Image

user = get_user_model().objects.get(username="test_user")

for _ in range(6):
    Image.objects.create(
        image_name="Image name",
        image_owner=user,
    )

images = Image.objects.all()
print(images)
