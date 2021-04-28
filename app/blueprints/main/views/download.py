from flask.views import View
from flask import send_file


class PDFDownload(View):
    """The PDFDownload class implements and endpoint to download the
    flask documentation in pdf format as attachment."""

    def dispatch_request(self):
        return send_file("blueprints/main/static/flask1.1.pdf", as_attachment=True)
