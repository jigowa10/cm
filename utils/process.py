import re
from janome.tokenizer import Tokenizer
import openai

def remove_furigana(text):
    text = re.sub(r'(\d+)（[^）]*）', r'\1', text)
    text = re.sub(r'([a-zA-Z]+)（([^）]*)）', r'\2', text)
    return text

def extract_cm_script(api_key, document_text):
    openai.api_key = api_key
    prompt = (
        "以下のWordファイルの内容から、CM原稿の本文部分のみを抽出してください。"
        "必要な情報は、本文のみであり、読み手の名前やメタデータ、その他の指示文は含めないでください。"
        "また、感想パートについては、5~7秒で読み上げられる短い一文のみを選んで残してください。"
        "読み手の名前は読み上げ部分ではないため除外してください。\n\n"
        f"{document_text}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.2,
    )
    return response['choices'][0]['message']['content']

def calculate_reading_time(script_text, words_per_minute=300, is_multiple_readers=False):
    tokenizer = Tokenizer()
    word_count = sum(1 for token in tokenizer.tokenize(script_text) if token.base_form not in ['\n', '', ' '])
    reading_time_seconds = (word_count / words_per_minute) * 60

    period_pause = script_text.count('。') * 0.2
    line_break_pause = script_text.count('\n') * (0.3 if is_multiple_readers else 0.7)
    phone_numbers = re.findall(r'\d+', script_text)
    phone_number_pause = sum(len(number) * 0.1 for number in phone_numbers)

    total_reading_time_seconds = reading_time_seconds + period_pause + line_break_pause + phone_number_pause
    return round(total_reading_time_seconds)
