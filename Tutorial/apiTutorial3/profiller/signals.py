from django.contrib.auth.models import User
from profiller.models import Profil, ProfilDurum
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
		ProfilDurum.objects.create(
			user_profil = instance,
			durum_mesaji = f'{instance.user.username} klübe katıldı.',
		)