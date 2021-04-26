from flask import Blueprint
from main.views.download import PDFDownload
from main.views.messages import MsgAPI
from main.views.index import IndexPage

main = Blueprint("main", __name__, template_folder="templates", static_folder="static")
main.add_url_rule("/", view_func=IndexPage.as_view("index"))
main.add_url_rule("/pdf", view_func=PDFDownload.as_view("pdf"))
main.add_url_rule("/msg", view_func=MsgAPI.as_view("msg"))
