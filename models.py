# File: models.py
from datetime import datetime, timedelta

class User:
    def __init__(self, user_id, nama, email, password, role):
        self.user_id = str(user_id)
        self.nama = str(nama)
        self.email = str(email)
        self.password = str(password)
        self.role = str(role)

# Pilar OOP: Abstraction & Inheritance
class BaseTicket:
    def __init__(self, ticket_number, user_id, uraian, dokumen=""):
        # Pilar OOP: Encapsulation
        self._ticket_number = str(ticket_number)
        self._user_id = str(user_id)
        self._support_id = "-"
        self._uraian = str(uraian)
        self._dokumen = str(dokumen)
        self._status = "Aduan Masuk"
        self._created_at = datetime.now()
        
        self._sla_deadline = self._created_at + timedelta(hours=48)

    # Getters
    def get_ticket_number(self): return self._ticket_number
    def get_user_id(self): return self._user_id
    def get_support_id(self): return self._support_id
    def get_uraian(self): return self._uraian
    def get_dokumen(self): return self._dokumen
    def get_status(self): return self._status
    def get_created_at_str(self): return self._created_at.strftime("%Y-%m-%d %H:%M:%S")
    def get_sla_str(self): return self._sla_deadline.strftime("%Y-%m-%d %H:%M:%S")

    # Setters (State Mutation)
    def set_support_id(self, support_id): self._support_id = str(support_id)
    def set_status(self, new_status): self._status = str(new_status)

    # Pilar OOP: Polymorphism (Akan di-override di child class)
    def get_kategori(self):
        pass

# Child Classes
class CSTicket(BaseTicket):
    def get_kategori(self): return "Customer Service"

class TechTicket(BaseTicket):
    def get_kategori(self): return "Technical Support"

class BillingTicket(BaseTicket):
    def get_kategori(self): return "Billing"

class SecurityTicket(BaseTicket):
    def get_kategori(self): return "Security"

class SalesTicket(BaseTicket):
    def get_kategori(self): return "Sales"

class LogEntry:
    def __init__(self, ticket_number, actor_id, status_sebelumnya, status_baru, pesan):
        self.log_id = "LOG-" + datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.ticket_number = str(ticket_number)
        self.actor_user_id = str(actor_id)
        self.status_by = str(actor_id)
        self.status_sebelumnya = str(status_sebelumnya)
        self.status_baru = str(status_baru)
        self.status = str(status_baru)
        self.pesan = str(pesan)
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")