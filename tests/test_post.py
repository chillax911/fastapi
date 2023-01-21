from typing import List
from app import schemas
import pytest
from app import models
from sqlalchemy import func

# def test_get_all_posts(authorized_client, test_posts):
#     res = authorized_client.get("/posts")

#     def validate(post):                         # Validation of the schema, covert dictionary into schema models.
#         return schemas.PostOut(**post)          # "Unpacks" the post
#     posts_map = map(validate, res.json())
#     posts_list = list(posts_map)
#     # print (list(posts_map))

#     assert len(res.json()) == len(test_posts)
#     assert res.status_code ==200

# def test_unauthorised_user_get_all_posts(client, test_posts):
#     res = client.get("/posts")
#     assert res.status_code == 401

# def test_unauthorised_user_get_one_posts(client, test_posts):
#     res = client.get(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401

# def test_get_one_post_not_exists(authorized_client, test_posts):
#     res = authorized_client.get(f"/posts/999")
#     assert res.status_code == 404

# def test_get_one_post(authorized_client, test_posts):  # These tests that the data unpacks correctly, and therefore is the structure is ok.
#     res = authorized_client.get(f"/posts/{test_posts[0].id}")
#     # print(res.json())
#     post = schemas.PostOut(**res.json())
#     # print (post)
#     assert post.Post.id == test_posts[0].id
#     assert post.Post.content == test_posts[0].content

# @pytest.mark.parametrize("title, content, published", [
#    ("awesome new title"  , "awesome new content" , True),
#    ("favorite pizza"     , "i love pepperoni"    , False),
#    ("tallest skyscrapers", "wahoo"               , True),
# ])
# def test_create_post(authorized_client, test_user, test_posts, title, content, published):
#    res = authorized_client.post(
#       "/posts/", json={"title": title, "content": content, "published": published})
#    created_post = schemas.Post(**res.json())
#    assert res.status_code == 201
#    assert created_post.title == title
#    assert created_post.content == content
#    assert created_post.published == published
#    assert created_post.owner_id == test_user['id']

# def test_create_post_default_publised_true(authorized_client, test_user, test_posts):
#    res = authorized_client.post(
#       "/posts/", json={"title": "any title", "content": "any content"})
#    created_post = schemas.Post(**res.json())
#    assert res.status_code == 201
#    assert created_post.title == "any title"
#    assert created_post.content == "any content"
#    assert created_post.published == True
#    assert created_post.owner_id == test_user['id']

# def test_unauthorised_user_create_post(client, test_posts):
#     res = client.post(
#         "/posts/", json={"title": "any title", "content": "any content"})
#     assert res.status_code == 401

def test_unauthorised_user_delete_post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts, session):
    qty_before = session.query(models.Post).count()   # print(f"Count BEFORE: {qty_before}")

    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")
    print("testing")

    qty_after = session.query(models.Post).count()   # print(f"Count AFTER: {qty_after}")
    qty_diff = qty_before - qty_after
    assert qty_diff == 1
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts, session):
    res = authorized_client.delete(
        f"/posts/999999")
    print("testing")
    assert res.status_code == 404

def test_delete_other_usesr_post(authorized_client, test_user, test_posts, session, test_user2):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
