from typing import List
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")

    def validate(post):                         # Validation of the schema, covert dictionary into schema models.
        return schemas.PostOut(**post)          # "Unpacks" the post
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    # print (list(posts_map))

    assert len(res.json()) == len(test_posts)
    assert res.status_code ==200

def test_unauthorised_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == 401

def test_unauthorised_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exists(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/999")
    assert res.status_code == 404 

def test_get_one_post(authorized_client, test_posts):  # These tests that the data unpacks correctly, and therefore is the structure is ok.
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    # print(res.json())
    post = schemas.PostOut(**res.json())
    # print (post)
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content 