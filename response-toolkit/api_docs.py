from tornado_swagger.model import register_swagger_model
from tornado import web


class HeartBeatHandler(web.RequestHandler):
    def get(self):
        """
        ---
        tags:
        - GET
        summary: Heartbeat
        description: Heartbeat handler allows to verify the activity of toolkit
        produces:
        - application/json
        responses:
            200:
              description: alive string
              schema:
                type: string
        """
        

class ServiceHandler(web.RequestHandler):
    def get(self):
        """
        ---
        tags:
        - GET
        summary: List services
        description: List all response strategies the toolkit is capable to handle
        produces:
        - application/json
        responses:
            200:
              description: list of services
              schema:
                type: array
        """

class StatusHandler(web.RequestHandler):

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
              $ref: '#/definitions/StatusModel'
        """


class RevokeJobHandler(web.RequestHandler):

    def post(self):
        """
        ---
        tags:
        - POST
        summary: Revoke Celery Job
        description: Allows to revoke actively running celery job by providing job ID
        produces:
        - application/json
        parameters:
        -   in: body
            name: body
            description: unique job identifier
            required: true
            schema:
              $ref: '#/definitions/RevokeModel'
        """


class CeleryTasks(web.RequestHandler):
    def post(self):
        """
        ---
        tags:
        - POST
        summary: Execute Celery Job
        description: Allows to manually execute a predefined celery job/process as response strategy
        produces:
        - application/json
        parameters:
        -   in: body
            name: body
            description: job data
            required: true
            schema:
              $ref: '#/definitions/CeleryModel'
        """


@register_swagger_model
class CeleryModel:
    """
    ---
    type: object
    description: Celery job name
    properties:
        task_name:
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

@register_swagger_model
class RevokeModel:
    """
    ---
    type: object
    description: Revocation model representation
    properties:
        job_uuid:
            type: string
    """