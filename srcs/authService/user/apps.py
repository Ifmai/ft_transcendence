from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from django.contrib.auth import get_user_model
        import user.signals
        User = get_user_model()

        if not User.objects.filter(username='ChatPolice').exists():
            User.objects.create_user(
                username='ChatPolice',
                password='ChatPolice123ChatPolice',
                email='ChatPolice@lastdance.com.tr',
                first_name='Muhammet Ali',
                last_name='Iskırık',
            )
