# OOP Workflow Helpdesk

Aplikasi helpdesk sederhana berbasis Flask dan Google Sheets. Proyek ini menunjukkan penerapan prinsip OOP dan beberapa design pattern dalam sistem yang fungsional.

## Ringkasan Arsitektur

Sistem menggunakan pemisahan tanggung jawab yang mirip MVC:

- **Routes/Controllers:** `app.py` menangani routing, session, dan render tampilan.
- **Domain Models:** `models.py` berisi `User`, `BaseTicket`, dan turunan tiket.
- **Workflow/Business Logic:** `workflow.py` menangani pembuatan tiket dan transisi status.
- **Data Access:** `database.py` mengabstraksi operasi CRUD ke Google Sheets.
- **Views:** template HTML di folder `templates/`.

```text
project-oop
├── app.py
├── database.py
├── docs
│   ├── architecture.mmd
│   └── presentation-points.md
├── models.py
├── oop-workflow-2d369154a481.json
├── README.md
├── requirements.txt
├── templates
│   ├── admin_dashboard.html
│   ├── base.html
│   ├── client_dashboard.html
│   ├── index.html
│   └── tracker.html
└── workflow.py
```

Alur data (tingkat tinggi):

1. Pengguna mengirim aksi lewat UI (client/admin).
2. `app.py` memanggil `WorkflowEngine` di `workflow.py`.
3. `WorkflowEngine` memperbarui data melalui `GoogleSheetManager` di `database.py`.
4. UI dirender ulang dengan data tiket/log terbaru.

## Pilar OOP (Contoh)

- **Enkapsulasi:** `BaseTicket` memakai atribut privat (contoh: `_status`) dengan getter/setter di `models.py`.
- **Abstraksi:** `BaseTicket` menyediakan antarmuka umum (`get_kategori()`), menyembunyikan detail implementasi.
- **Pewarisan:** `CSTicket`, `TechTicket`, `BillingTicket`, `SecurityTicket`, dan `SalesTicket` mewarisi `BaseTicket`.
- **Polimorfisme:** `get_kategori()` di-override pada tiap child class, namun digunakan dengan cara yang sama.

## Design Pattern yang Digunakan

- **Factory Pattern:** `TicketFactory.create()` memilih subclass tiket berdasarkan kategori.
- **State-like Transition:** `WorkflowEngine.process_action()` memusatkan transisi status dan pencatatan log.

## Implementasi Modularitas

Modularitas diterapkan dengan memisahkan tanggung jawab ke beberapa modul:

- `app.py` sebagai pengendali alur (routing, session, render view).
- `models.py` sebagai representasi domain (User dan Ticket).
- `workflow.py` sebagai logika bisnis dan transisi status.
- `database.py` sebagai lapisan akses data ke Google Sheets.
- `templates/` untuk tampilan UI.

## Cara Menjalankan

1. Install dependensi:

```bash
pip install -r requirements.txt
```

2. Pastikan kredensial Google Sheets tersedia:

- Letakkan `oop-workflow-2d369154a481.json` di root proyek (jangan di-commit).
- Pastikan Google Sheet dibagikan ke email service account.

3. Jalankan aplikasi:

```bash
python app.py
```

Buka di browser:
- Client: `http://127.0.0.1:5001/client`
- Admin: `http://127.0.0.1:5001/admin`

## Catatan Deployment

- Jangan commit file kredensial Google.
- Gunakan `SECRET_KEY` yang aman untuk production.
