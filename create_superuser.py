import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

User = get_user_model()

def create_superuser():
    username = 'AbouDA'
    email = 'abokordaoud22@gmail.com'
    password = 'Newabou22'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f'Superuser {username} created successfully!')
    else:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f'Superuser {username} password updated successfully!')

if __name__ == '__main__':
    create_superuser()
