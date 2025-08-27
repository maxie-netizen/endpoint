# app.py (main application file)
import os
import re
import requests
import yt_dlp
from flask import Flask, request, jsonify, send_file, render_template
from urllib.parse import quote, unquote
import uuid
import threading
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.secret_key = os.urandom(24)

# Ensure download directory exists
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# YouTube downloader function
def download_youtube_video(url, format_type='video', quality='best'):
    try:
        download_id = str(uuid.uuid4())
        download_path = os.path.join(app.config['DOWNLOAD_FOLDER'], download_id)
        os.makedirs(download_path, exist_ok=True)
        
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'quiet': True,
        }
        
        if format_type == 'audio':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            if quality == 'best':
                ydl_opts['format'] = 'best[height<=1080]'  # Limit to 1080p max
            elif quality == '720p':
                ydl_opts['format'] = 'best[height<=720]'
            elif quality == '480p':
                ydl_opts['format'] = 'best[height<=480]'
            elif quality == '360p':
                ydl_opts['format'] = 'best[height<=360]'
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)
            
            if format_type == 'audio':
                downloaded_file = os.path.splitext(downloaded_file)[0] + '.mp3'
            
            return {
                'success': True,
                'file_path': downloaded_file,
                'title': info.get('title', 'Unknown'),
                'id': download_id
            }
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Search YouTube function
def search_youtube(query, max_results=5):
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_json': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search YouTube using the query
            search_results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
            
            if not search_results or 'entries' not in search_results:
                return {'success': False, 'error': 'No results found'}
            
            results = []
            for entry in search_results['entries']:
                if entry:  # Skip None entries
                    results.append({
                        'title': entry.get('title', 'Unknown'),
                        'url': entry.get('url', ''),
                        'thumbnail': entry.get('thumbnail', ''),
                        'duration': entry.get('duration', 0),
                        'uploader': entry.get('uploader', 'Unknown')
                    })
            
            return {'success': True, 'results': results}
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Instagram downloader function (simplified example)
def download_instagram(url):
    try:
        # This is a simplified example - you might need a dedicated Instagram API library
        # Note: Instagram has strict scraping policies
        download_id = str(uuid.uuid4())
        download_path = os.path.join(app.config['DOWNLOAD_FOLDER'], download_id)
        os.makedirs(download_path, exist_ok=True)
        
        # Using a hypothetical Instagram download approach
        # In reality, you'd need to handle authentication and API limits
        response = requests.get(url)
        
        # This is a placeholder - actual implementation would require more complex parsing
        # or using a dedicated service/API for Instagram downloads
        video_url = None
        
        # Very basic regex to find video URLs (this may not work for all cases)
        video_patterns = [
            r'"video_url":"([^"]+)"',
            r'<meta property="og:video" content="([^"]+)"',
            r'src="([^"]+\.mp4)"'
        ]
        
        for pattern in video_patterns:
            match = re.search(pattern, response.text)
            if match:
                video_url = match.group(1)
                break
        
        if not video_url:
            return {'success': False, 'error': 'Could not find media URL'}
        
        # Download the video
        video_response = requests.get(video_url, stream=True)
        filename = secure_filename(f"instagram_{download_id}.mp4")
        file_path = os.path.join(download_path, filename)
        
        with open(file_path, 'wb') as f:
            for chunk in video_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return {
            'success': True,
            'file_path': file_path,
            'title': f"Instagram Video {download_id}",
            'id': download_id
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

# TikTok downloader function (simplified example)
def download_tiktok(url):
    try:
        # Similar to Instagram, TikTok requires special handling
        # This is a simplified example
        download_id = str(uuid.uuid4())
        download_path = os.path.join(app.config['DOWNLOAD_FOLDER'], download_id)
        os.makedirs(download_path, exist_ok=True)
        
        # Using a hypothetical approach
        # In reality, you might use a service like https://rapidapi.com/ 
        # or a dedicated TikTok API wrapper
        
        # Placeholder implementation
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        
        # Try to find video URL in page source
        video_url = None
        video_patterns = [
            r'"downloadAddr":"([^"]+)"',
            r'"playAddr":"([^"]+)"',
            r'<video src="([^"]+)"',
            r'src="([^"]+\.mp4)"'
        ]
        
        for pattern in video_patterns:
            match = re.search(pattern, response.text)
            if match:
                video_url = match.group(1).replace('\\u002F', '/')
                break
        
        if not video_url:
            return {'success': False, 'error': 'Could not find media URL'}
        
        # Download the video
        video_response = requests.get(video_url, headers=headers, stream=True)
        filename = secure_filename(f"tiktok_{download_id}.mp4")
        file_path = os.path.join(download_path, filename)
        
        with open(file_path, 'wb') as f:
            for chunk in video_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return {
            'success': True,
            'file_path': file_path,
            'title': f"TikTok Video {download_id}",
            'id': download_id
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Cleanup function to remove old files
def cleanup_old_files():
    import time
    import shutil
    while True:
        time.sleep(3600)  # Run every hour
        try:
            now = time.time()
            for filename in os.listdir(app.config['DOWNLOAD_FOLDER']):
                file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
                if os.path.isdir(file_path):
                    # Remove folders older than 24 hours
                    if os.path.getmtime(file_path) < now - 24 * 3600:
                        shutil.rmtree(file_path)
        except Exception as e:
            print(f"Cleanup error: {e}")

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search')
def search_api():
    query = request.args.get('q')
    platform = request.args.get('platform', 'youtube')
    
    if not query:
        return jsonify({'success': False, 'error': 'No search query provided'})
    
    if platform == 'youtube':
        result = search_youtube(query)
        return jsonify(result)
    else:
        return jsonify({'success': False, 'error': f'Search not supported for {platform}'})

@app.route('/api/download')
def download_api():
    url = request.args.get('url')
    platform = request.args.get('platform')
    format_type = request.args.get('format', 'video')
    quality = request.args.get('quality', 'best')
    
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'})
    
    if platform == 'youtube':
        result = download_youtube_video(url, format_type, quality)
    elif platform == 'instagram':
        result = download_instagram(url)
    elif platform == 'tiktok':
        result = download_tiktok(url)
    else:
        return jsonify({'success': False, 'error': 'Unsupported platform'})
    
    return jsonify(result)

@app.route('/download/<file_id>')
def download_file(file_id):
    try:
        # Security check to prevent directory traversal
        if '../' in file_id or file_id not in os.listdir(app.config['DOWNLOAD_FOLDER']):
            return "File not found", 404
        
        folder_path = os.path.join(app.config['DOWNLOAD_FOLDER'], file_id)
        if not os.path.isdir(folder_path):
            return "File not found", 404
        
        # Find the first file in the directory
        files = os.listdir(folder_path)
        if not files:
            return "File not found", 404
        
        file_path = os.path.join(folder_path, files[0])
        safe_filename = secure_filename(files[0])
        
        return send_file(file_path, as_attachment=True, download_name=safe_filename)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
