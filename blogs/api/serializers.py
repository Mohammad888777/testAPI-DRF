from rest_framework import serializers
from rest_framework.serializers import ValidationError
from ..models import Blog



class BlogSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=Blog
        fields=[
            "id",
            "title",
            "created",
            "image",
            "slug"
        ]

        extra_kwargs={
            "id":{"read_only":True},
            "title":{"read_only":True},
            "created":{"read_only":True},
            "image":{"read_only":True},
            "slug":{"read_only":True},
        }
    



class EachBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model=Blog
        fields=[
            "id",
            "title",
            "created",
            "image",
            "slug",
            "description",
            "description_show",
            
        ]

        extra_kwargs={
            "id":{"read_only":True},
            "title":{"read_only":True},
            "created":{"read_only":True},
            "image":{"read_only":True},
            "slug":{"read_only":True},
            "description":{"read_only":True},
            "description_show":{"read_only":True},
        }