from rest_framework import serializers

from ..models import ReviewRating,ReviewBlog



class SubReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReviewRating
        fields=[
            'id',
            'review',
            'rating',
            'is_active',
            'child'
        ]

        extra_kwargs={
            'id':{"read_only":True},
            'review':{"required":True},
            'category':{"read_only":True},
            'parent':{"read_only":True},
            # 'is_active':{"read_only":True},
            'rating':{"required":True},
            'child':{"read_only":True}
        }

    
    def validate_review(self,value):
        if len(value)<3:
            raise serializers.ValidationError("lenght of value must be over than 3")
        return value
    
    def validate_rating(self,value):
        if not 0<=value<=5:
            raise serializers.ValidationError("rating must be between 0 to 5")
        return value

    
    def create(self, validated_data:dict):
        new_rev=ReviewRating(
            review=validated_data.get("review"),
            rating=validated_data.get("rating"),
            is_active=False
        )
        new_rev.save()
        return new_rev



class ReviewSerializer(serializers.ModelSerializer):
    child=SubReviewSerializer(many=True)
    class Meta:
        model=ReviewRating
        fields=[
            'id',
            'review',
            'rating',
            'category',
            'parent',
            'is_active',
            'child'
        ]

        extra_kwargs={
            'id':{"read_only":True},
            'review':{"read_only":True},
            'category':{"read_only":True},
            'parent':{"read_only":True},
            'is_active':{"read_only":True},
            'rating':{"read_only":True},
        }
        # depth=2












class SubBlogReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReviewBlog
        fields=[
            'id',
            'review',
            'blog',
            'is_active',
            'name',
            'email',
            'review',

            'child'
        ]

        extra_kwargs={
            'id':{"read_only":True},
            'review':{"required":True},
            'category':{"read_only":True},
            # 'parent':{"read_only":True},
            # 'is_active':{"read_only":True},
            'child':{"read_only":True},
            'email':{"read_only":True},
            'name':{"read_only":True},
            'blog':{"read_only":True},
        }

    
    def validate_review(self,value):
        if len(value)<3:
            raise serializers.ValidationError("lenght of value must be over than 3")
        return value
    

    
    def create(self, validated_data:dict):
        new_rev=ReviewBlog(
            review=validated_data.get("review"),
            is_active=False
        )
        new_rev.save()
        return new_rev
    








class ReviewBlogSerializer(serializers.ModelSerializer):
    child=SubBlogReviewSerializer(many=True)

    class Meta:
        model=ReviewBlog
        fields=[
             'id',
            'review',
            'blog',
            'is_active',
            'name',
            'email',
            'review',
            'parent',

            'child'
        ]

        extra_kwargs={

            'id':{"read_only":True},
            'review':{"required":True},
            'category':{"read_only":True},
            'parent':{"read_only":True},
            'child':{"read_only":True},
            'email':{"read_only":True},
            'name':{"read_only":True},
            'blog':{"read_only":True},
        }