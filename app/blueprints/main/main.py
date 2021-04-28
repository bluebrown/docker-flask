from flask import Blueprint
from blueprints.main.views.download import PDFDownload
from blueprints.main.views.messages import MsgAPI
from blueprints.main.views.index import IndexPage

blueprint = Blueprint("main", __name__, static_folder="static")
blueprint.add_url_rule("/", view_func=IndexPage.as_view("index"))
blueprint.add_url_rule("/pdf", view_func=PDFDownload.as_view("pdf"))
blueprint.add_url_rule("/msg", view_func=MsgAPI.as_view("msg"))
