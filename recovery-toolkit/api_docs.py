from tornado_swagger.model import register_swagger_model
from tornado import web


class PostsHandler(web.RequestHandler):
    def get(self):
        """
        ---
        tags:
        - Posts
        summary: List posts
        description: List all posts in feed
        produces:
        - application/json
        responses:
            200:
              description: list of posts
              schema:
                type: array
                items:
                  $ref: '#/definitions/PostModel'
        """

    def post(self):
        """
        ---
        tags:
        - Posts
        summary: Add posts
        description: Add posts in feed
        produces:
        - application/json
        parameters:
        -   in: body
            name: body
            description: post data
            required: true
            schema:
              $ref: '#/definitions/PostModel'
        """


class PostsDetailsHandler(web.RequestHandler):
    def get(self, posts_id):
        """
        ---
        tags:
        - Posts
        summary: Get posts details
        description: posts full version
        produces:
        - application/json
        parameters:
        -   name: posts_id
            in: path
            description: ID of post to return
            required: true
            type: string
        responses:
            200:
              description: list of posts
              schema:
                $ref: '#/definitions/PostModel'
        """

    def patch(self, posts_id):
        """
        ---
        tags:
        - Posts
        summary: Edit posts
        description: Edit posts details
        produces:
        - application/json
        parameters:
        -   name: posts_id
            in: path
            description: ID of post to edit
            required: true
            type: string
        -   in: body
            name: body
            description: post data
            required: true
            schema:
              $ref: '#/definitions/PostModel'
        """

    def delete(self, posts_id):
        """
        ---
        tags:
        - Posts
        summary: Delete posts
        description: Remove posts from feed
        produces:
        - application/json
        parameters:
        -   name: posts_id
            in: path
            description: ID of post to delete
            required: true
            type: string
        """


@register_swagger_model
class PostModel:
    """
    ---
    type: object
    description: Post model representation
    properties:
        id:
            type: integer
            format: int64
        title:
            type: string
        text:
            type: string
        is_visible:
            type: boolean
            default: true
    """
