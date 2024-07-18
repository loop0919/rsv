from flask import render_template


def register_error_handlers(app):
    @app.errorhandler(400)
    def error_400(error):
        return render_template('error/400.html')

    @app.errorhandler(404)
    def error_404(error):
        return render_template('error/404.html')
