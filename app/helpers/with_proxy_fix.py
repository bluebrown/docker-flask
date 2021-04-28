import re
from werkzeug.middleware.proxy_fix import ProxyFix


def with_proxy_fix(app):
    """The with_proxy_fix function applies the werkzeug proxyfix if the
    PROXY_FIX environment variable has been set.
    e.g. PROXY_FIX='x_for=1 x_host=1 x_port=1 x_prefix=1 x_proto=1'"""

    proxy_fix = app.config.get("PROXY_FIX")

    if proxy_fix:
        kwargs = {
            k: int(v.strip('"')) for k, v in re.findall(r'(\S+)=(".*?"|\S+)', proxy_fix)
        }
        app.logger.debug(f"parsed PROXY_FIX: {kwargs}")
        app.wsgi_app = ProxyFix(app.wsgi_app, **kwargs)

    return app
