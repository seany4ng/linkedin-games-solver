from flask import jsonify
from core.app import create_app
from core.app.exceptions import APIException

app = create_app()


# Global error handler
@app.errorhandler(APIException)
def handle_exception(e: APIException):
    return jsonify({"error": e.message}), e.status_code


if __name__ == "__main__":
    for rule in app.url_map.iter_rules():
            print(f"Route: {rule.rule}, Methods: {', '.join(rule.methods)}, Endpoint: {rule.endpoint}")
    app.run(host="localhost", port=8000, debug=True)
