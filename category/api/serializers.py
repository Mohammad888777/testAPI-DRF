from rest_framework import serializers
from ..models import Category,Teacher,TeacherFeather
from django.db.models import Avg,Count
from reviews.api.serializers import ReviewSerializer
from datetime import datetime




class TeacherFeatherSerializer(serializers.ModelSerializer):

    class Meta:
        model=TeacherFeather
        fields=[
            'detail'
        ]

class CategoryFirstSerializer(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields=[
            'id',
            'name',
            'url'
        ]

        extra_kwargs={
            'id':{"read_only":True},
            'name':{"read_only":True},
            'url':{"lookup_field":"id","view_name":"each-category"}
        }

        


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    teacher_name=serializers.CharField(source="teacher.name")
    teacher_image=serializers.CharField(source="teacher.image")
    parent=CategoryFirstSerializer()
    avg=serializers.FloatField(required=False)
    saved_in=serializers.BooleanField(default=False)
    add_to_cart=serializers.BooleanField(default=False)

    def count_ordered(self,obj):
        pass
    # return obj.order_set.all().count()

    


    class Meta:
        model=Category

        fields=[
            'id',
            'name',
            'avg',
            'image',
            'teacher_name',
            'teacher_image',
            'parent',
            'price',
            'show_price',
            'saved_in',
            'add_to_cart',
            'category_type'
        ]
        depth=2
        



class FreeCatSerializer(serializers.HyperlinkedModelSerializer):

    teacher_name=serializers.CharField(source="teacher.name")
    teacher_image=serializers.CharField(source="teacher.image")
    teacher__fetch=TeacherFeatherSerializer(
        source="teacher.teacherfeather_set",many=True
    )
    # parent=CategoryFirstSerializer()
    # cc=serializers.FloatField(required=False)
    # saved_in=serializers.BooleanField(default=False)
    # add_to_cart=serializers.BooleanField(default=False)

    def count_ordered(self,obj):
        pass
    # return obj.order_set.all().count()

    


    class Meta:
        model=Category

        fields=[
            'id',
            'name',
            # 'cc',
            'image',
            'teacher_name',
            'teacher_image',
            'teacher__fetch',
            
            # 'parent',
            # 'price',
            # 'show_price',
            # 'saved_in' ,
            # 'add_to_cart',
            'category_type'
        ]
        depth=2





class EachPaySerializer(serializers.ModelSerializer):
    teacher_name=serializers.CharField(source="teacher.name")
    teacher_image=serializers.CharField(source="teacher.image")
    parent=CategoryFirstSerializer()
    avg=serializers.FloatField(required=False)
    saved_in=serializers.BooleanField(default=False)
    add_to_cart=serializers.BooleanField(default=False)
    has_videos=serializers.BooleanField(default=False)
    has_voices=serializers.BooleanField(default=False)
    has_files=serializers.BooleanField(default=False)

    time_s_created=serializers.SerializerMethodField(
        method_name="time_s"
    )

    def count_ordered(self,obj):
        pass
    # return obj.order_set.all().count()

    def time_s(self,obj:Category):
        return datetime.timestamp(obj.created)


    


    class Meta:
        model=Category

        fields=[
            'id',
            'name',
            'avg',
            'teacher_name',
            'teacher_image',
            'parent',
            'price',
            'show_price',
            'saved_in',
            'add_to_cart',
            'category_type',
            'ckedit',
            'package_contacts',
            'subject',
            'category_duration',
            'session_numbers',
            'description',
            'product_type',
            'pre_review',
            'image',
            'created',
            'time_s_created',
            'has_videos',
            'has_voices',
            'has_files',

        ]
        depth=2
        extra_kwargs={
            'pre_review':{"allow_null":True,"read_only":True},
            'image':{"allow_null":True,"read_only":True},
            'name':{"read_only":True},
            'created':{"read_only":True},
            'product_type':{"read_only":True},
            'description':{"read_only":True,"allow_null":True},
            'session_numbers':{"read_only":True,"allow_null":True},
            'category_duration':{"read_only":True,"allow_null":True},
            'subject':{"read_only":True,"allow_null":True},
            'package_contacts':{"read_only":True,"allow_null":True},
            'ckedit':{"read_only":True,"allow_null":True},
     

        }
        


