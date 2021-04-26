from flask.views import View
from flask import send_file


class PDFDownload(View):
    def dispatch_request(self):
        return send_file("main/static/flask1.1.pdf", as_attachment=True)
