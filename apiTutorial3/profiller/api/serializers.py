from profiller.models import Profil, ProfilDurum
from rest_framework import serializers


class ProfilSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    foto = serializers.ImageField(read_only=True)
    
    class Meta:
        model = Profil
        fields = '__all__'


class ProfilPhotoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profil
        fields = ('foto',)

class ProfilDurunSerializer(serializers.ModelSerializer):
    user_profil = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProfilDurum
        fields = '__all__'
