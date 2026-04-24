import factory
from customauth.models import CustomUser
from .models import Post, Category, Comment


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        django_get_or_create = ('email',)   # 同じemailのユーザーが存在すれば取得、

    name = factory.Faker('name', locale='ja')
    email = factory.Faker('ascii_email')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    
    slug = factory.Faker('slug')
    title = factory.Faker('text', locale='ja', max_nb_chars=20)
    body = factory.Faker('paragraph', locale='ja')
    author = factory.Faker('random_element', elements=list(CustomUser.objects.filter(is_admin=1)))
    category = factory.Faker('random_element', elements=list(Category.objects.all()))


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post_id = factory.Faker('random_element', elements=list(Post.objects.all()))
    author = factory.Faker('random_element', elements=list(CustomUser.objects.all()))
    body = factory.Faker('paragraph', locale='ja')
    