import docx
import re

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    full_text = [para.text for para in doc.paragraphs]
    return '\n'.join(full_text)

def extract_broadcast_info(document_text):
    broadcast_info = {}
    patterns = {
        "番組名": r"【\s*番\s*組\s*名\s*】\s*(.*?)\n",
        "放送日時": r"【\s*放送日時／秒数\s*】\s*(.*?)\n",
        "営業担当": r"【\s*営業担当\s*】\s*(.*?)\n",
        "スポンサー名": r"【\s*スポンサー名\s*】\s*(.*?)\n",
        "商品内容": r"【\s*商品内容\s*】\s*(.*?)\n",
        "読み手": r"【\s*読み手\s*】\s*(.*?)\n",
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, document_text)
        if match:
            broadcast_info[key] = match.group(1).strip()
    
    return broadcast_info
