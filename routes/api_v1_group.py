from flask_openapi3 import APIBlueprint

v1_group = APIBlueprint('v1_group', __name__, url_prefix='/api/v1')
