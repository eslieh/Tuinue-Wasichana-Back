from flask import Blueprint, request, jsonify
import cloudinary
import cloudinary.uploader
import os
cloudinary_bp = Blueprint('cloudinary_bp', __name__)

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)
@cloudinary_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        result = cloudinary.uploader.upload(file)
        return jsonify({"url": result['secure_url']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
