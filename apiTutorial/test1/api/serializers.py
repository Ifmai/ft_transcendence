from rest_framework import serializers
from test1.models import Makale, Gazateci
from datetime import datetime
from datetime import date
from django.utils.timesince import timesince




class MakaleSerializer(serializers.ModelSerializer):
	time_since_pub = serializers.SerializerMethodField()
	#yazar = serializers.StringRelatedField()
	#yazar = GazetiSerializer()

	class Meta:
		model = Makale
		fields = '__all__'
		read_only_fields = ['id', 'yaratilma_tarihi', 'güncelleneme_tarihi']

	def get_time_since_pub(self, object):
		now = datetime.now()
		pub_date = object.yayımlanma_tarihi
		if object.aktif == True:
			time_delta = timesince(pub_date, now)
			return time_delta
		else:
			return 'Aktif Değil.'
	
	def validate_yayımlanma_tarihi(self, value):
		today = date.today()
		if value > today:
			raise serializers.ValidationError('Yayınlanma tarihi bugünden ileri bir tarih olamaz.')
		return value


class GazetiSerializer(serializers.ModelSerializer):
	#makaleler = MakaleSerializer(many=True, read_only=True)
	makaleler = serializers.HyperlinkedRelatedField(
		many=True,
		read_only=True,
		view_name='makale-details'
	)
	class Meta:
		model = Gazateci
		fields = '__all__'












# Standart Default Serializers 
class MakaleDefaultSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	yazar = serializers.CharField()
	baslik = serializers.CharField()
	aciklama = serializers.CharField()
	metin = serializers.CharField()
	sehir = serializers.CharField()
	yayımlanma_tarihi = serializers.DateField()
	aktif = serializers.BooleanField()
	yaratilma_tarihi = serializers.DateTimeField(read_only=True) # bir şey yapma demek istiyoruz.
	güncelleneme_tarihi  = serializers.DateTimeField(read_only=True)


	def create(self, validated_data):
		print(validated_data);
		return Makale.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.yazar = validated_data.get('yazar', instance.yazar)
		instance.baslik = validated_data.get('baslik', instance.baslik)
		instance.aciklama = validated_data.get('aciklama', instance.aciklama)
		instance.metin = validated_data.get('metin', instance.metin)
		instance.sehir = validated_data.get('sehir', instance.sehir)
		instance.yayımlanma_tarihi = validated_data.get('yayımlanma_tarihi', instance.yayımlanma_tarihi)
		instance.aktif = validated_data.get('aktif', instance.aktif)
		instance.save()
		return instance
		#yayınlanma tarihi vb. otomatik bu yüzden onlar manuel değişmiyor.
		#bu yüzden eklemiyoruz onları buraya.
	

	#object level da bütün datayı alıyoruz.
	def validate(self, data): #object level
		if data['baslik'] == data['aciklama']:
			raise serializers.ValidationError('Baslik ve Aciklama alanları aynı olamaz. Lüften farklı bir açıklama giriniz.')
		return data
	

	#Burada value ile işlem yapıyoruz
	def validate_baslik(self, value):
		if len(value) < 20:
			raise serializers.ValidationError(f'Minimum başlık alanı 20 karakter olmalıdır. Siz {len(value)} karakter girdiniz.')
		return value