# My Comment Library

A library for adding comments to models using Django REST Framework.

## Installation
```bash
pip install my_comment_library
```

## Usage

```python
from drf_comments.comments import BaseComment, CommentViewSet, comment_serializer, create_comment_serializer

# Define your models
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PostComment(BaseComment):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta(BaseComment.Meta):
        db_table = 'posts_postcomment'
        verbose_name = 'Post Comment'
        verbose_name_plural = 'Post Comments'

# Define your serializers
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at']

PostCommentSerializer = comment_serializer(PostComment)
PostCommentCreateSerializer = create_comment_serializer(PostComment)

# Define your viewsets
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class PostCommentViewSet(CommentViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    create_serializer_class = PostCommentCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]