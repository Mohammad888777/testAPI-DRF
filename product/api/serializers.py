from rest_framework import serializers
from ..models import ProductVideo,ProductFile,ProductVoice


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductVideo
        fields=[
            'id',
            'is_active',
            'created',
            'part',
            'category',
            'video_duration',
            'video_link'
        ]

        extra_kwargs={
            'id':{"read_only":True},
            'is_active':{"read_only":True},
            'created':{"read_only":True},
            'part':{"read_only":True},
            'category':{"read_only":True},
            'video_duration':{"read_only":True},
            'video_link':{"read_only":True},
        }
    



class VoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductVoice
        fields=[
            'id',
            'is_active',
            'created',
            'part',
            'category',
            'voice_duration',
            'voice_link'
        ]

        extra_kwargs={
            'id':{"read_only":True},
            'is_active':{"read_only":True},
            'created':{"read_only":True},
            'part':{"read_only":True},
            'category':{"read_only":True},
            'voice_duration':{"read_only":True},
            'voice_link':{"read_only":True},
        }






class FileProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductFile
        fields=[
            'id',
            'is_active',
            'created',
            'part',
            'category',
            'file_name',
            'product_file'
        ]

        extra_kwargs={
            'id':{"read_only":True},
            'is_active':{"read_only":True},
            'created':{"read_only":True},
            'part':{"read_only":True},
            'category':{"read_only":True},
            'file_name':{"read_only":True},
            'product_file':{"read_only":True},
        }