from flask import Flask, request, render_template
from utils.extract import extract_text_from_docx, extract_broadcast_info
from utils.process import remove_furigana, calculate_reading_time, extract_cm_script
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        api_key = os.getenv('OPENAI_API_KEY')
        file_path = './uploads/temp.docx'
        file.save(file_path)

        document_text = extract_text_from_docx(file_path)
        document_text = remove_furigana(document_text)
        broadcast_info = extract_broadcast_info(document_text)
        is_multiple_readers = '×' in broadcast_info.get('読み手', '')

        cm_script = extract_cm_script(api_key, document_text)
        reading_time = calculate_reading_time(cm_script, is_multiple_readers=is_multiple_readers)

        return render_template('index.html', broadcast_info=broadcast_info, cm_script=cm_script, reading_time=reading_time)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
