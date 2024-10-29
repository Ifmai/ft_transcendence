from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        import user.signals
        post_migrate.connect(create_default_user)

def create_default_user(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username='ChatPolice').exists():
        User.objects.create_user(
            username='ChatPolice',
            password='ChatPolice123ChatPolice',
            email='ChatPolice@10.11.22.5',
            first_name='Muhammet Ali',
            last_name='Iskırık',
        )
