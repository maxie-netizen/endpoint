import uuid
from flask import Blueprint, request, jsonify
from models import User, APIKey, DownloadHistory
from extensions import db   # <-- better: create extensions.py with db, bcrypt, login_manager
from datetime import datetime
from functools import wraps

# Define Blueprint
api = Blueprint('api', __name__)

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')

        if not api_key:
            return jsonify({'error': 'API key required'}), 401

        # Check if API key is valid
        key_record = APIKey.query.filter_by(key=api_key, is_active=True).first()

        if not key_record:
            return jsonify({'error': 'Invalid API key'}), 401

        if key_record.expires_at < datetime.utcnow():
            return jsonify({'error': 'API key has expired'}), 401

        # Attach user_id to request context
        request.user_id = key_record.user_id
        return f(*args, **kwargs)

    return decorated_function


@api.route('/api/download/youtube', methods=['GET'])
@api_key_required
def download_youtube():
    url = request.args.get('url')
    format_type = request.args.get('format', 'video')
    quality = request.args.get('quality', 'best')

    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        # Placeholder download simulation
        result = {
            'success': True,
            'url': url,
            'format': format_type,
            'quality': quality,
            'download_url': f'/downloads/youtube/{uuid.uuid4()}.mp4'
        }

        # Log the download
        download = DownloadHistory(
            user_id=request.user_id,
            platform='youtube',
            url=url,
            format=format_type,
            status='success'
        )
        db.session.add(download)
        db.session.commit()

        return jsonify(result)

    except Exception as e:
        # Log failed download
        download = DownloadHistory(
            user_id=request.user_id,
            platform='youtube',
            url=url,
            format=format_type,
            status='failed'
        )
        db.session.add(download)
        db.session.commit()

        return jsonify({'error': str(e)}), 500


# Instagram
@api.route('/api/download/instagram', methods=['GET'])
@api_key_required
def download_instagram():
    return jsonify({'message': 'Instagram download endpoint (to be implemented)'})


# TikTok
@api.route('/api/download/tiktok', methods=['GET'])
@api_key_required
def download_tiktok():
    return jsonify({'message': 'TikTok download endpoint (to be implemented)'})
