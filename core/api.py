"""Define the api application."""

from flask import Blueprint, jsonify, request

from core.services.exifs_reader_service import ExifsReaderService

urls_blueprint = Blueprint("api_urls", __name__)


@urls_blueprint.route("/", methods=["GET"])
def home_default():
    """Define a test page to check the webservice is up and running at root url."""
    return "Page par defaut", 200


@urls_blueprint.route("/exif-reader-api/api/v0.0.1a", methods=["GET"])
def home():
    """Define a test page to check the webservice is up and running at ws url."""
    return (
        "Welcome to this weather forecast application.",
        200,
    )


@urls_blueprint.route(
    "/exif-reader-api/api/v0.0.1a/get-exif", methods=["POST"]
)
def get_exif():
    """Define the method to set an email as a spam or a ham."""
    payload = request.get_json(force=True)

    if "image-source" not in payload.keys():
        result = {
            "status": "ko",
            "message": "The source image must be indicated !",
        }
        return jsonify(result), 200

    exifs_info = ExifsReaderService(
        **{
            "image-source": payload["image-source"],
        }
    )
    payload_response = exifs_info.get_full_exifs()
    print(payload_response)

    return jsonify(payload_response), 200
