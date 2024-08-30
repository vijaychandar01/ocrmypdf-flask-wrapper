from flask import Blueprint, render_template, request, send_file, redirect, url_for, session, jsonify
from app.processing import process_pdfs
from werkzeug.utils import secure_filename
from threading import Thread
import os
import uuid

main_bp = Blueprint('main', __name__)

progress = {}
stop_signals = {}

@main_bp.route('/')
def index():
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    return render_template('index.html', session_id=session_id)

@main_bp.route('/upload', methods=['POST'])
def upload():
    session_id = session.get('session_id')
    uploaded_files = request.files.getlist("file[]")
    selected_languages = request.form.getlist('languages')
    skip_big = request.form.get('skip_big', 50)
    optimize = request.form.get('optimize', 0)
    ocr_option = request.form.get('ocr_option', 'skip')

    if not selected_languages:
        return "Please select at least one language.", 400

    language_flag = '+'.join(selected_languages)
    uploaded_file_paths = []

    for file in uploaded_files:
        if file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploaded_file_paths.append(file_path)

    thread = Thread(target=process_pdfs, args=(session_id, uploaded_file_paths, language_flag, skip_big, optimize, ocr_option))
    thread.start()

    return redirect(url_for('main.progress_page', session_id=session_id))

@main_bp.route('/progress/<session_id>')
def progress_page(session_id):
    if progress.get(session_id, {}).get('percent', 0) == 100:
        return redirect(url_for('main.download', session_id=session_id))
    return render_template('progress.html', session_id=session_id)

@main_bp.route('/status/<session_id>')
def status(session_id):
    return jsonify(progress.get(session_id, {'percent': 0, 'filename': 'No file being processed'}))

@main_bp.route('/stop/<session_id>', methods=['POST'])
def stop(session_id):
    stop_signals[session_id] = True
    return jsonify({'status': 'stopped'})

@main_bp.route('/download/<session_id>')
def download(session_id):
    zip_filepath = os.path.join(current_app.config['PROCESSED_FOLDER'], 'processed_pdfs.zip')
    files_processed = progress.get(session_id, {}).get('percent', 0)

    if files_processed == 0:
        return redirect(url_for('main.index'))

    if files_processed < 100:
        return render_template('partial_download.html', session_id=session_id)

    if os.path.exists(zip_filepath):
        return send_file(zip_filepath, as_attachment=True)
    
    return redirect(url_for('main.index'))

@main_bp.route('/partial-download/<session_id>', methods=['POST'])
def partial_download(session_id):
    download_choice = request.form.get('download_choice')
    zip_filepath = os.path.join(current_app.config['PROCESSED_FOLDER'], 'processed_pdfs.zip')

    if download_choice == 'yes' and os.path.exists(zip_filepath):
        return send_file(zip_filepath, as_attachment=True)
    
    return redirect(url_for('main.index'))
