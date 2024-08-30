import os
import ocrmypdf
import tempfile
import shutil
import zipfile
from PyPDF2 import PdfReader, PdfWriter
from app.routes import progress, stop_signals

def process_pdfs(session_id, uploaded_file_paths, language_flag, skip_big, optimize, ocr_option):
    processed_files = []
    total_files = len(uploaded_file_paths)
    progress[session_id] = {
        'percent': 0,
        'filename': '',
        'ocr_progress': 0,
        'current_file_index': 0,
        'total_files': total_files,
        'pages_done': 0,
        'total_pages': 0,
    }
    
    stop_signals[session_id] = False

    for i, file_path in enumerate(uploaded_file_paths):
        if stop_signals[session_id]:
            break

        filename = os.path.basename(file_path)
        output_path = os.path.join(current_app.config['PROCESSED_FOLDER'], filename)
        temp_folder = tempfile.mkdtemp(dir=current_app.config['PROCESSED_FOLDER'])

        reader = PdfReader(file_path)
        total_pages = len(reader.pages)

        progress[session_id]['filename'] = filename
        progress[session_id]['total_pages'] = total_pages
        progress[session_id]['current_file_index'] = i
        progress[session_id]['pages_done'] = 0

        for page_num in range(total_pages):
            if stop_signals[session_id]:
                break

            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])
            single_page_path = os.path.join(temp_folder, f"page_{page_num + 1}.pdf")
            
            with open(single_page_path, 'wb') as temp_pdf:
                writer.write(temp_pdf)

            ocrmypdf.ocr(
                single_page_path, 
                single_page_path.replace('.pdf', '_ocr.pdf'), 
                language=language_flag, 
                skip_text=ocr_option == 'skip', 
                force_ocr=ocr_option == 'force',  
                redo_ocr=ocr_option == 'redo',
                skip_big=int(skip_big),  
                optimize=int(optimize)
            )

            progress[session_id]['ocr_progress'] = ((page_num + 1) / total_pages) * 100
            progress[session_id]['pages_done'] = page_num + 1

        if not stop_signals[session_id]:
            with open(output_path, 'wb') as output_pdf:
                writer = PdfWriter()
                for page_num in range(total_pages):
                    processed_page_path = os.path.join(temp_folder, f"page_{page_num + 1}_ocr.pdf")
                    with open(processed_page_path, 'rb') as processed_pdf:
                        reader = PdfReader(processed_pdf)
                        writer.add_page(reader.pages[0])
                writer.write(output_pdf)

            processed_files.append(output_path)
            progress[session_id]['percent'] = ((i + 1) / total_files) * 100

        shutil.rmtree(temp_folder)

    if processed_files:
        zip_filename = 'processed_pdfs.zip'
        zip_filepath = os.path.join(current_app.config['PROCESSED_FOLDER'], zip_filename)
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for processed_file in processed_files:
                zipf.write(processed_file, os.path.basename(processed_file))
                os.remove(processed_file)

        progress[session_id]['percent'] = 100
    else:
        progress[session_id]['percent'] = 0
