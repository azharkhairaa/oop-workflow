# Poin Presentasi (Ringkas)

## 1) Arsitektur & Modularitas
- Struktur terpisah: routes (`app.py`), domain model (`models.py`), workflow (`workflow.py`), data access (`database.py`), dan UI (`templates/`).
- Alur data jelas: UI -> routes -> workflow -> database -> UI.

## 2) Pilar OOP
- Encapsulation: atribut privat & getter/setter di `BaseTicket`.
- Abstraction: `BaseTicket` jadi kontrak dasar tiket.
- Inheritance: kelas ticket mewarisi `BaseTicket`.
- Polymorphism: `get_kategori()` di-override di tiap child class.

## 3) Design Pattern
- Factory Pattern untuk pembuatan tiket berdasarkan kategori.
- State-like workflow untuk transisi status (terpusat di `WorkflowEngine`).
