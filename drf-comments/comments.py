from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from rest_framework import serializers, viewsets

from django.db import models
from django.conf import settings
from rest_framework import serializers, viewsets

class BaseComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        abstract = True

    def __str__(self):
        return f'Comment by {self.user}'

    def children(self):
        return self.__class__.objects.filter(parent=self)

    @property
    def is_parent(self):
        return self.parent is None

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'user', 'text', 'created_at', 'updated_at', 'replies', 'parent']

    def get_replies(self, obj):
        if obj.is_parent:
            return self.__class__(obj.children(), many=True).data
        return None

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'user', 'text', 'parent']

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            data['user'] = request.user
        data['parent'] = data.get('parent', None)
        return data

def comment_serializer(amodel):
    class DynamicCommentSerializer(CommentSerializer):
        class Meta(CommentSerializer.Meta):
            model = amodel
            fields = list(CommentSerializer.Meta.fields)
            if hasattr(amodel, 'object'):
                fields.append('object')

    return DynamicCommentSerializer

def create_comment_serializer(amodel):
    class DynamicCommentCreateSerializer(CommentCreateSerializer):
        class Meta(CommentCreateSerializer.Meta):
            model = amodel
            fields = list(CommentCreateSerializer.Meta.fields)
            if hasattr(amodel, 'object'):
                fields.append('object')

    return DynamicCommentCreateSerializer

class CommentViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return self.create_serializer_class
        return self.serializer_class
