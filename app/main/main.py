from flask import Blueprint

from main.views.download import PDFDownload
from main.views.messages import MsgAPI


main = Blueprint("main", __name__)
main.add_url_rule("/pdf", view_func=PDFDownload.as_view("pdf"))
main.add_url_rule("/msg", view_func=MsgAPI.as_view("msg"))
