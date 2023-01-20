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
