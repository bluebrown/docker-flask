import re
from werkzeug.middleware.proxy_fix import ProxyFix


def with_proxy_fix(app):
    proxy_fix = app.config.get("PROXY_FIX")
    if proxy_fix:
        kwargs = {
            k: int(v.strip('"')) for k, v in re.findall(r'(\S+)=(".*?"|\S+)', proxy_fix)
        }
        app.logger.debug(f"parsed PROXY_FIX: {kwargs}")
        app.wsgi_app = ProxyFix(app.wsgi_app, **kwargs)
    return app
