import sys
import os 
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent 
GOOGLE_CREDS_PATH = BASE_DIR / "config" / "credentials.json"
SPREADSHEET_ID = os.getenv('SPREADSHEET_KEY')

def test_google_sheets():
    """Тест подключения к Google Sheets"""
    try:
        print(f"🔄 Рабочая директория: {Path.cwd()}")
        print(f"🔄 Путь к credentials: {GOOGLE_CREDS_PATH}")
        print(f"🔄 Файл существует: {GOOGLE_CREDS_PATH.exists()}")
        print(f"🔄 ID таблицы: {SPREADSHEET_ID}") 

        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            str(GOOGLE_CREDS_PATH),
            scope
        )
        client = gspread.authorize(creds)

        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        sheet.append_row(["Тест ID", "Тестовый товар", "Успешный тест!"])
        
        print("\n✅ Данные записаны в таблицу!")
        print(f"🔗 Ссылка: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")

    except Exception as e:
        print(f"\n❌ Ошибка: {repr(e)}", file=sys.stderr)
        if hasattr(e, 'response'):
            print(f"Детали: {e.response.text}", file=sys.stderr)

if __name__ == "__main__":
    test_google_sheets()