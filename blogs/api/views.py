from rest_framework.response import Response
from rest_framework.generics import GenericAPIView,ListAPIView,RetrieveAPIView
from rest_framework.serializers import ValidationError
from ..models import Blog
from .serializers import BlogSerializer,EachBlogSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q




class HomeViewBlogs(ListAPIView):
    def get_queryset(self):
        return Blog.objects.filter(
            is_active=True
        ).order_by("-created")[:4]
    
    def get_serializer_class(self):
        return BlogSerializer
    
    
    

class EachBlog(
    RetrieveAPIView
)    :
    
    def get_queryset(self):
        return Blog.objects.filter(
            is_active=True
        )
    
    def get_object(self):
        q=self.get_queryset()
        b=get_object_or_404(q,id=self.kwargs.get("id"))
        return b
    
    def get(self, request, *args, **kwargs):
        o=self.get_object()

        related=Blog.objects.filter(
            is_active=True
        ).filter(
            Q(title__icontains=o.title)|
            Q(description_show__icontains=o.description_show)|
            Q(slug__icontains=o.slug)
        ).order_by("created")
        z=[]
        rel_ser=BlogSerializer(instance=related,many=True)
        own=EachBlogSerializer(o)
        z.extend([rel_ser.data,own.data])

        return Response(z)
    



