# -*- coding:utf-8 -*-
from graphene import relay, ObjectType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from blog.models import Post


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        only_fields = ('title', 'content',)
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        if info.context.user.is_anonymous:
            return queryset.filter(published=True)
        return queryset

    @classmethod
    def get_node(cls, info, id):
        try:
            post = cls._meta.model.objects.get(id=id)
        except cls._meta.model.DoesNotExist:
            return None

        if post.published or info.context.user == post.owner:
            return post
        return None


class Query(ObjectType):
    all_posts = DjangoFilterConnectionField(PostNode)
    my_posts = DjangoFilterConnectionField(PostNode)

    def resolve_all_posts(self, info):
        return Post.objects.filter(published=True)

    def resolve_my_posts(self, info):
        if not info.context.user.is_authenticated():
            return Post.objects.none()
        else:
            return Post.objects.filter(owner=info.context.user)
