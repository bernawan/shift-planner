import sqlite3

def init_db():
    """Inisialisasi database dan tabel shift"""
    conn = sqlite3.connect("shift_data.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS shift (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            username TEXT NOT NULL,
            pengganti TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def tambah_shift(tanggal, username, pengganti):
    """Menambahkan data shift yang baru"""
    conn = sqlite3.connect("shift_data.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO shift (tanggal, username, pengganti) VALUES (?, ?, ?)",
                (tanggal, username, pengganti))
    conn.commit()
    conn.close()

def get_shift_by_tanggal(tanggal):
    """Mengambil data shift berdasarkan tanggal"""
    conn = sqlite3.connect("shift_data.db")
    cur = conn.cursor()
    cur.execute("SELECT username, pengganti FROM shift WHERE tanggal = ?", (tanggal,))
    result = cur.fetchall()
    conn.close()
    return result
