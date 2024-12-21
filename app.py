import logging

from flask_openapi3 import Info
from flask_openapi3 import OpenAPI
#from routes import host_extraction, v1_group, home
from routes import vm_extraction, v1_group, home
#from routes import containerpod_extraction, v1_group, home
from tools import check_startup

info = Info(title="Instana Compatibility Matrix API", version="1.0.0")
app = OpenAPI(__name__, info=info)
logger = logging.getLogger(__name__)

# Configuration check
app.config.from_object('config.default')
check_startup(app)

# V1 Api registration
#v1_group.register_api(host_extraction)
v1_group.register_api(vm_extraction)
#v1_group.register_api(containerpod_extraction)
app.register_api(v1_group)

app.register_api(home)








if __name__ == '__main__':
    app.run(debug=True, use_debugger=True)
