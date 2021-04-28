from werkzeug.utils import find_modules, import_string
from os import walk


def register_blueprints(app):
    """register all blueprints in the blueprints folder.
    It will look for an object named "blueprint" in those files."""
    for blueprint in next(walk("blueprints"))[1]:
        for name in find_modules(f"blueprints.{blueprint}"):
            mod = import_string(name)
            if hasattr(mod, "blueprint"):
                app.register_blueprint(mod.blueprint)
