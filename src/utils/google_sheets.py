import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config.settings import GOOGLE_CREDS_PATH, SPREADSHEET_ID
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GoogleSheetClient:
    def __init__(self):
        """Инициализация клиента Google Sheets"""
        try:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                str(GOOGLE_CREDS_PATH),
                scope
            )
            self.client = gspread.authorize(creds)
        except Exception as e:
            logger.error(f"Ошибка инициализации Google Sheets: {e}")
            raise

    def append_data(self, data: list[dict]):
        """Добавляет данные в таблицу"""
        try:
            sheet = self.client.open_by_key(SPREADSHEET_ID).sheet1
            
            # Подготовка заголовков если лист пустой
            if not sheet.get_all_values():
                sheet.append_row(["ID", "Название", "Описание", "Исходные данные"])
            
            # Добавление данных
            rows = []
            for item in data:
                rows.append([
                    item.get("id", ""),
                    item.get("name", ""),
                    item.get("description", ""),
                    item.get("source_text", "")
                ])
            
            if rows:
                sheet.append_rows(rows)
                logger.info(f"Добавлено {len(rows)} строк в таблицу")
            else:
                logger.warning("Нет данных для добавления")

        except Exception as e:
            logger.error(f"Ошибка добавления данных: {e}")
            raise