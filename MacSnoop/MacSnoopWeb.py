from waitress import serve


class web_server():
    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in'  : 'header',
            'name': 'X-API-KEY'
        }
    }

    @staticmethod
    def web_app():
        from flask import Flask
        from flask_restplus import Resource, Api

        app = Flask(__name__)
        api = Api(app, doc='/docs', prefix="/api/v1", authorizations=web_server.authorizations, security='apikey', )
        api_v1 = api.namespace('some-thing', description='It does the thing')

        @api.route('/hello')
        class HelloWorld(Resource):
            def get(self):
                return {'hello': 'world'}

        @api_v1.route("/<int:id>")
        class Conference(Resource):
            def get(self, id):
                """
                Displays a conference's details
                """

            def put(self, id):
                """
                Edits a selected conference
                """

        serve(app, listen='*:8080')


if __name__ == '__main__':
    web_server.web_app()
