from django.contrib.auth.models import User
from user.models import Profil, ProfileComment
from django.db.models.signals import post_save
from django.dispatch import receiver

#Alıcı(receiver) User da bir kaydetme işleminden sonra çalışacak.
@receiver(post_save, sender=User)
def create_profil(sender, instance, created, **kwargs):
	print(instance.username , '__Created: ', created )
	if created:
		Profil.objects.create(user=instance)


@receiver(post_save, sender=Profil)
def create_first_durum(sender, instance, created, **kwargs):
	print(instance.user.username , '__Created: ', created )
	if created:
		ProfileComment.objects.create(
			user_profil = instance,
			comment_text = f'{instance.user.username} attended the last dance ball..',
		)

# @receiver(post_save, sender=User)
# def create_refresh_token(sender, instance, created, **kwargs):
# 	print(instance.user.username , '__Created: ', created )
# 	if created:
# 		RefreshToken.objects.create(
# 			auth_user = instance,
# 			token = f'',
# 		)