from server import app

import controllers.auth as auth
import controllers.api as api
import controllers.view as view


app.add_url_rule('/', view_func=view.index, methods=['GET'], strict_slashes=False)