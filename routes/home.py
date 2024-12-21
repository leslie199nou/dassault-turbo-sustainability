from flask_openapi3 import APIBlueprint, Tag
from flask import redirect

tag = Tag(name='Home', description="Get redirected to the Swagger page")
#home = APIBlueprint('host_extraction', __name__, abp_tags=[tag])
home = APIBlueprint('vm_extraction', __name__, abp_tags=[tag])
#home = APIBlueprint('containerpod_extraction', __name__, abp_tags=[tag])

@home.get('/',)
def home_to_doc():
    """This endpoint will just redirect to the swagger page"""
    return redirect('/openapi/')
