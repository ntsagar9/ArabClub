from django.contrib.auth import get_user_model

model = get_user_model()


def create_user():
    for i in range(1700, 1000000):
        data = {
            'username': f'test_user_auto_{i}',
            'email': f'test_user_{i}@mail.com',
            'date_of_birth': '1998-7-13',
            'password': '123'
        }

        user = model.objects.create_user(**data)
        print(f'Create Done ID --> {user.id} username --> {user.username})')
        print('-'*50)