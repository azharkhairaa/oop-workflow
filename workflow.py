# File: workflow.py
from datetime import datetime
import random
from models import CSTicket, SalesTicket, SecurityTicket, TechTicket, BillingTicket, LogEntry

# Design Pattern: Factory Pattern
class TicketFactory:
    @staticmethod
    def create(kategori, user_id, uraian, dokumen=""):
        ticket_number = "TIX-" + datetime.now().strftime("%Y%m%d") + str(random.randint(100, 999))
        if kategori == "Customer Service":
            return CSTicket(ticket_number, user_id, uraian, dokumen)
        elif kategori == "Technical Support":
            return TechTicket(ticket_number, user_id, uraian, dokumen)
        elif kategori == "Billing":
            return BillingTicket(ticket_number, user_id, uraian, dokumen)
        elif kategori == "Security":
            return SecurityTicket(ticket_number, user_id, uraian, dokumen)
        elif kategori == "Sales":
            return SalesTicket(ticket_number, user_id, uraian, dokumen)
        else:
            return CSTicket(ticket_number, user_id, uraian, dokumen) # Default fallback

# OOP Workflow Engine
class WorkflowEngine:
    def __init__(self, db_manager):
        self.db = db_manager

    def submit_aduan(self, kategori, user_id, uraian, dokumen):
        # Buat tiket via Factory
        ticket = TicketFactory.create(kategori, user_id, uraian, dokumen)
        self.db.insert_ticket(ticket)
        
        # Log awal
        log = LogEntry(ticket.get_ticket_number(), user_id, "-", ticket.get_status(), "Pelanggan membuat aduan baru.")
        self.db.insert_log(log)
        return ticket.get_ticket_number()

    # Design Pattern: State Pattern (logika transisi status)
    def process_action(self, ticket_number, action_type, actor_id, current_status, pesan, target_divisi=None, actor_role=None):
        new_status = current_status
        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        support_id = actor_id

        # Routing State berdasar aksi
        if action_type == "TINDAK_LANJUT":
            new_status = "Dalam Penanganan"
        elif action_type == "DISPOSISI":
            new_status = "Disposisi"
            role_label = actor_role or "-"
            pesan = f"Disposisi dari divisi {role_label} ke divisi {target_divisi}. Pesan: {pesan}"
            support_id = target_divisi
        elif action_type == "TANYA_USER":
            new_status = "Menunggu tanggapan Pelanggan"
        elif action_type == "BALASAN_USER":
            new_status = "Menunggu tanggapan Admin"
            support_id = None
        elif action_type == "SELESAI":
            new_status = "Aduan selesai"

        # Update DB
        self.db.update_ticket_db(ticket_number, support_id, new_status, waktu_sekarang)
        
        # Rekam Log
        log = LogEntry(ticket_number, actor_id, current_status, new_status, pesan)
        self.db.insert_log(log)