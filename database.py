# File: database.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from models import User, LogEntry

class GoogleSheetManager:
    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name("oop-workflow-2d369154a481.json", scope)
            # creds = ServiceAccountCredentials.from_json_keyfile_name("ticket-bot-495712-345c6f94b6ad.json", scope)
            self.client = gspread.authorize(creds)
            # URL Google Sheets
            self.sheet = self.client.open_by_url("https://docs.google.com/spreadsheets/d/193Ca9lvhwtNXzB6hh-iX6NyhEG980FS0noH6kk0zb_M/edit")
        except Exception as e:
            print("Gagal koneksi GSheets:", e)
            self.sheet = None

    def get_user_by_email(self, email):
        ws = self.sheet.worksheet("users")
        for row in ws.get_all_records():
            if str(row["email"]) == str(email):
                return User(row["id"], row["nama"], row["email"], row["password"], row["role"])
        return None

    def get_user_by_id(self, user_id):
        ws = self.sheet.worksheet("users")
        for row in ws.get_all_records():
            if str(row["id"]) == str(user_id):
                return User(row["id"], row["nama"], row["email"], row["password"], row["role"])
        return None

    def get_user_by_role(self, role):
        ws = self.sheet.worksheet("users")
        for row in ws.get_all_records():
            if str(row["role"]) == str(role):
                return User(row["id"], row["nama"], row["email"], row["password"], row["role"])
        return None

    def insert_user(self, user):
        ws = self.sheet.worksheet("users")
        ws.append_row([user.user_id, user.nama, user.email, user.password, user.role])

    def insert_ticket(self, ticket):
        ws = self.sheet.worksheet("pengaduan")
        db_id = "DBT-" + datetime.now().strftime("%Y%m%d%H%M%S")
        ws.append_row([
            db_id, ticket.get_ticket_number(), ticket.get_user_id(), ticket.get_support_id(),
            ticket.get_kategori(), ticket.get_uraian(), ticket.get_dokumen(),
            ticket.get_status(), ticket.get_sla_str(), ticket.get_created_at_str(), ticket.get_created_at_str()
        ])

    def get_all_tickets(self):
        ws = self.sheet.worksheet("pengaduan")
        return ws.get_all_records()

    def update_ticket_db(self, ticket_number, support_id, new_status, current_time_str):
        ws = self.sheet.worksheet("pengaduan")
        records = ws.get_all_records()
        for idx, row in enumerate(records):
            if str(row["ticket_number"]) == str(ticket_number):
                row_idx = idx + 2
                if support_id is not None:
                    ws.update_cell(row_idx, 4, str(support_id)) # support_by_user_id
                ws.update_cell(row_idx, 8, str(new_status)) # status
                ws.update_cell(row_idx, 11, str(current_time_str)) # updated_at
                break

    def insert_log(self, log):
        ws = self.sheet.worksheet("pengaduan_log")
        ws.append_row([
            log.log_id, log.ticket_number, log.status, log.actor_user_id,
            log.status_sebelumnya, log.status_baru, log.pesan, log.created_at, log.status_by
        ])
        
    def get_logs_by_ticket(self, ticket_number):
        ws = self.sheet.worksheet("pengaduan_log")
        logs = []
        for row in ws.get_all_records():
            if str(row["ticket_number"]) == str(ticket_number):
                logs.append(row)
        return logs