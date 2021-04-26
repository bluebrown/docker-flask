from flask import Blueprint
from flask import render_template
from main.views.download import PDFDownload
from main.views.messages import MsgAPI

main = Blueprint("main", __name__, template_folder="templates")
main.add_url_rule("/pdf", view_func=PDFDownload.as_view("pdf"))
main.add_url_rule("/msg", view_func=MsgAPI.as_view("msg"))


@main.route("/")
def index():
    return render_template("index.html")
