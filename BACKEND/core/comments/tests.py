import pytest

from core.fixtures.user import user
from core.fixtures.post import post
from core.comments.models import Comment


@pytest.mark.django_db
def test_create_comment(user, post):
    comment = Comment.objects.create(author=user, post=post, body='Test comment Body')
    assert comment.author == user
    assert comment.post == post
    assert comment.body == 'Test comment Body'