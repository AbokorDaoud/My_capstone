import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.contrib.auth.models import User

def reset_superuser():
    username = 'AbokorDaoud'  # Your username
    password = 'Newabokor22'  # Your password
    email = 'abokordaoud22@gmail.com'  # Your email

    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"Password reset successfully for user {username}")
    except User.DoesNotExist:
        user = User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Created new superuser {username}")

if __name__ == '__main__':
    reset_superuser()
