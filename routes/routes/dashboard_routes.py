from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import dashboard, db
from models import APIKey, DownloadHistory
from datetime import datetime, timedelta
import secrets

@dashboard.route('/dashboard')
@login_required
def dashboard():
    api_keys = APIKey.query.filter_by(user_id=current_user.id).all()
    download_history = DownloadHistory.query.filter_by(user_id=current_user.id).order_by(DownloadHistory.downloaded_at.desc()).limit(10).all()
    return render_template('dashboard.html', api_keys=api_keys, download_history=download_history)

@dashboard.route('/api-keys')
@login_required
def api_keys():
    api_keys = APIKey.query.filter_by(user_id=current_user.id).all()
    return render_template('api_keys.html', api_keys=api_keys)

@dashboard.route('/generate-api-key', methods=['POST'])
@login_required
def generate_api_key():
    name = request.form.get('name')
    expiry_days = int(request.form.get('expiry_days', 30))
    
    # Generate a unique API key
    key = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=expiry_days)
    
    api_key = APIKey(
        key=key,
        user_id=current_user.id,
        name=name,
        expires_at=expires_at
    )
    
    db.session.add(api_key)
    db.session.commit()
    
    flash(f'API key generated successfully: {key}')
    return redirect(url_for('dashboard.api_keys'))

@dashboard.route('/revoke-api-key/<int:key_id>')
@login_required
def revoke_api_key(key_id):
    api_key = APIKey.query.get(key_id)
    
    if api_key and api_key.user_id == current_user.id:
        api_key.is_active = False
        db.session.commit()
        flash('API key revoked successfully')
    
    return redirect(url_for('dashboard.api_keys'))
