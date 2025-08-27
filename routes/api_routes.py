from flask import request, jsonify
from app import api, db
from models import User, APIKey, DownloadHistory
from datetime import datetime
from functools import wraps

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
        
        # Add user to request context
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
    
    # Your YouTube download logic here
    # This is a placeholder - implement your actual download logic
    try:
        # Simulate download process
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

# Similar endpoints for Instagram and TikTok
@api.route('/api/download/instagram', methods=['GET'])
@api_key_required
def download_instagram():
    # Implement Instagram download logic
    pass

@api.route('/api/download/tiktok', methods=['GET'])
@api_key_required
def download_tiktok():
    # Implement TikTok download logic
    pass
  
