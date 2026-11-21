"""Indikator berbasis aturan. Ditampilkan TERPISAH dari prediksi model (sesuai proposal).
Keberadaan satu indikator saja tidak membuktikan pesan adalah penipuan.
21/11/2026 20:30
Menambah saran untuk rules desakan waktu dan mengaku instansi lalu menambah 2 rules baru: paket palsu dan ganti nomor.
"""
import re

RULES = [
    ("permintaan_transfer", "Permintaan transfer uang",
     r"\b(transfer|tf|kirim uang|rekening|rek\.?|no\.? ?rek|dana|top ?up)\b"),
    ("permintaan_kode_rahasia", "Permintaan kode OTP/PIN/password",
     r"\b(otp|kode verifikasi|kode 6|pin|password|kata sandi|cvv)\b"),
    ("tautan", "Mengandung tautan",
     r"(https?://|www\.|bit\.ly|wa\.me|\b[\w-]+\.(com|id|xyz|site|online|click|top|vip|icu|net)\b)"),
    ("file_apk", "Meminta membuka/instal file aplikasi (.apk)", r"\.apk\b"),
    ("klaim_hadiah", "Klaim hadiah/undian",
     r"\b(hadiah|undian|pemenang|menang|giveaway|cek tunai|voucher|cashback)\b"),
    ("ancaman_blokir", "Ancaman pemblokiran/penonaktifan akun",
     r"\b(blokir|diblokir|nonaktif|dinonaktifkan|ditutup|dibekukan|hangus|ditangguhkan)\b"),
    ("desakan_waktu", "Desakan untuk segera bertindak",
     r"\b(segera|sekarang juga|hari ini|24 jam|1x24|sebelum pukul|secepatnya|urgent|buruan|batas waktu)\b"),
    ("biaya_di_muka", "Meminta biaya di muka (admin/pajak/ongkir)",
     r"\b(biaya (admin|administrasi|pendaftaran|pencairan|pajak|pengiriman)|ongkir|deposit|uang jaminan)\b"),
    ("mengaku_instansi", "Mengatasnamakan bank/instansi/perusahaan",
     r"\b(bca|bri|bni|mandiri|bsi|ojk|bpjs|kemensos|pajak|djp|polri|pln|telkomsel|shopee|tokopedia|dana|ovo|gopay)\b"),
    ("paket_palsu", "Mengaku soal paket/kurir bermasalah",
     r"\b(paket|resi|kurir|jne|j&t|sicepat|anteraja)\b.{0,80}\b(gagal|tertahan|tidak terkirim|konfirmasi alamat)\b"),
    ("ganti_nomor", "Mengaku ganti nomor / kerabat minta bantuan",
     r"\b(ganti nomor|nomor baru|no baru|hp (lama )?(rusak|hilang)|nomor lama)\b"),
]
_COMPILED = [(k, label, re.compile(p, re.I | re.S)) for k, label, p in RULES]

SARAN = {
    "permintaan_transfer": "Jangan mentransfer uang sebelum memverifikasi pengirim melalui saluran resmi!",
    "permintaan_kode_rahasia": "Jangan pernah membagikan kode OTP, PIN, atau password kepada siapa pun!",
    "tautan": "Jangan langsung membuka tautan. Cek alamat situs resmi secara manual!",
    "file_apk": "Jangan mengunduh atau menginstal file .apk dari pesan, karena bisa mencuri data!",
    "klaim_hadiah": "Hadiah resmi tidak pernah meminta biaya di muka. Cek ke kanal resmi penyelenggara.",
    "ancaman_blokir": "Cek status akun langsung lewat aplikasi atau situs resmi, bukan lewat tautan di pesan.",
    "biaya_di_muka": "Waspadai permintaan biaya di muka, ini pola umum penipuan!",
    "desakan_waktu": "Tenangkan diri. Pastikan kebenaran pesan sebelum bertindak dan jangan terburu-buru.",
    "mengaku_instansi": "Hubungi instansi lewat nomor atau aplikasi resmi, dan jangan membagikan data pribadi lewat pesan!",
    "paket_palsu": "Lacak status paket lewat aplikasi, situs resmi, dan jangan membagikan nomor resi atau data pribadi lewat pesan!",
    "ganti_nomor": "Telepon nomor lama kerabat tersebut untuk memastikan sebelum mengirim uang.",
}


def find_indicators(text: str) -> list[dict]:
    return [{"kode": k, "keterangan": label} for k, label, rx in _COMPILED if rx.search(text)]


def build_advice(indicators: list[dict], label: str) -> list[str]:
    adv = [SARAN[i["kode"]] for i in indicators if i["kode"] in SARAN]
    if label == "indikasi penipuan" and not adv:
        adv.append("Verifikasi pengirim melalui saluran resmi sebelum menanggapi pesan ini.")
    if label == "belum dapat dipastikan":
        adv.append("Hasil belum pasti. Tetap berhati-hati dan verifikasi lewat saluran resmi.")
    return adv
