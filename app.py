# File: app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import GoogleSheetManager
from workflow import WorkflowEngine
from models import User
import random

app = Flask(__name__)
app.secret_key = "kunci_rahasia_untuk_session_flask"

# Inisialisasi Database dan Engine
db = GoogleSheetManager()
engine = WorkflowEngine(db)

@app.route("/", methods=["GET", "POST"])
def index():
    if "user_id" in session:
        if session["user_role"] == "Client":
            return redirect(url_for("client_dashboard"))
        else:
            return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        action = request.form.get("action")
        
        # Proses Login
        if action == "login":
            email = request.form.get("email")
            password = request.form.get("password")
            user = db.get_user_by_email(email)
            
            if user and user.password == password:
                # Simpan data di session browser
                session["user_id"] = user.user_id
                session["user_nama"] = user.nama
                session["user_role"] = user.role
                return redirect(url_for("index"))
            else:
                flash("Email atau password salah!", "danger")
                
        # Proses Registrasi
        elif action == "register":
            nama = request.form.get("nama")
            email = request.form.get("email")
            password = request.form.get("password")
            new_id = "USR-" + str(random.randint(10000, 99999))
            
            new_user = User(new_id, nama, email, password, "Client")
            db.insert_user(new_user)
            flash("Registrasi berhasil! Silakan login.", "success")

    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/client", methods=["GET", "POST"])
def client_dashboard():
    if "user_id" not in session or session["user_role"] != "Client":
        return redirect(url_for("index"))

    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "buat_tiket":
            kategori = request.form.get("kategori")
            uraian = request.form.get("uraian")
            dokumen = request.form.get("dokumen")
            
            tix_num = engine.submit_aduan(kategori, session["user_id"], uraian, dokumen)
            flash("Tiket berhasil dibuat dengan nomor: " + tix_num, "success")
            
        elif action == "balas_tiket":
            ticket_number = request.form.get("ticket_number")
            balasan = request.form.get("balasan")
            current_status = request.form.get("current_status")
            
            engine.process_action(ticket_number, "BALASAN_USER", session["user_id"], current_status, balasan)
            flash("Balasan terkirim.", "success")

    # Ambil tiket milik user yang sedang login
    semua_tiket = db.get_all_tickets()
    tiket_saya = []
    for t in semua_tiket:
        if str(t["ticket_by_user_id"]) == str(session["user_id"]):
            t["riwayat_pesan"] = db.get_logs_by_ticket(t["ticket_number"])
            tiket_saya.append(t)
            print(f"Logs for {t['ticket_number']}: {t['riwayat_pesan']}")

    return render_template("client_dashboard.html", tiket_saya=tiket_saya)

@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    if "user_id" not in session or session["user_role"] == "Client":
        return redirect(url_for("index"))

    if request.method == "POST":
        ticket_number = request.form.get("ticket_number")
        current_status = request.form.get("current_status")
        tindakan = request.form.get("tindakan")
        pesan = request.form.get("pesan")
        divisi_tujuan = request.form.get("divisi_tujuan")
        
        # Eksekusi State Pattern di Workflow Engine
        engine.process_action(
            ticket_number,
            tindakan,
            session["user_id"],
            current_status,
            pesan,
            target_divisi=divisi_tujuan,
            actor_role=session["user_role"],
        )
        flash("Status tiket berhasil diupdate!", "success")

    semua_tiket = db.get_all_tickets()
    tiket_terkait = []
    
    # Filter: admin hanya lihat kategori sendiri, plus disposisi masuk/keluar divisinya
    role_divisi = session["user_role"]
    for t in semua_tiket:
        if t["status"] == "Aduan selesai":
            continue

        logs = db.get_logs_by_ticket(t["ticket_number"])
        is_role_ticket = str(t.get("jenis_pengaduan")) == str(role_divisi)
        is_disposisi_masuk = any(
            (log.get("status_baru") == "Disposisi")
            and (f"Disposisi ke divisi {role_divisi}" in str(log.get("pesan", "")))
            for log in logs
        )
        is_disposisi_keluar = any(
            (log.get("status_baru") == "Disposisi")
            and (f"Disposisi dari divisi {role_divisi} ke divisi" in str(log.get("pesan", "")))
            for log in logs
        )

        if is_role_ticket or is_disposisi_masuk or is_disposisi_keluar:
            t["riwayat_pesan"] = logs
            tiket_terkait.append(t)

    return render_template("admin_dashboard.html", tiket_terkait=tiket_terkait)

@app.route("/tracker", methods=["GET", "POST"])
def tracker():
    tiket_ditemukan = None
    logs = []
    
    if request.method == "POST":
        cari_nomor = request.form.get("ticket_number")
        semua_tiket = db.get_all_tickets()
        
        for t in semua_tiket:
            if str(t["ticket_number"]) == str(cari_nomor):
                tiket_ditemukan = t
                logs = db.get_logs_by_ticket(cari_nomor)
                break
                
        if not tiket_ditemukan:
            flash("Tiket tidak ditemukan.", "danger")

    return render_template("tracker.html", tiket=tiket_ditemukan, logs=logs)

if __name__ == "__main__":
    app.run(debug=True, port=5001)