import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tes Gaya Hidup & Harapan Hidup", layout="centered")

st.markdown("""
# 🧬 Tes Gaya Hidup, Risiko, dan Harapan Hidup
Isi kuis ini untuk mengetahui **tingkat risiko kesehatan dan perkiraan harapan hidup** kamu.  
Jawab sejujur mungkin ya — hasil ini bersifat edukatif, bukan diagnosis medis.
""")

st.divider()

# ------------------------------
# Pertanyaan (17 parameter)
# ------------------------------
questions = {
    # --- A. Fisik ---
    "Pola makan": {
        "question": "Seberapa sering kamu makan sayur, buah, dan makanan rumahan (bukan instan)?",
        "options": ["Hampir setiap hari", "Beberapa kali seminggu", "Jarang", "Hampir tidak pernah"],
        "scores": [100, 80, 50, 20],
    },
    "Aktivitas fisik": {
        "question": "Berapa kali kamu berolahraga (minimal 30 menit) dalam seminggu?",
        "options": ["5 kali atau lebih", "2–4 kali", "1 kali", "Jarang / tidak pernah"],
        "scores": [100, 80, 50, 20],
    },
    "Tidur": {
        "question": "Rata-rata berapa jam kamu tidur berkualitas setiap malam?",
        "options": ["7–8 jam", "5–6 jam", "Kurang dari 5 jam", "Sering bergadang"],
        "scores": [100, 80, 50, 20],
    },
    "Berat badan": {
        "question": "Bagaimana kondisi berat badanmu saat ini?",
        "options": ["Ideal", "Sedikit berlebih / kurang", "Berlebih (obesitas ringan)", "Obesitas / terlalu kurus"],
        "scores": [100, 80, 50, 20],
    },
    "Asupan air": {
        "question": "Berapa banyak air putih yang kamu minum per hari?",
        "options": [">8 gelas", "6–8 gelas", "3–5 gelas", "<3 gelas"],
        "scores": [100, 80, 50, 20],
    },

    # --- B. Kebiasaan berisiko ---
    "Merokok": {
        "question": "Apakah kamu merokok?",
        "options": ["Tidak pernah", "Sudah berhenti", "Kadang-kadang", "Ya, rutin"],
        "scores": [100, 90, 60, 20],
    },
    "Alkohol": {
        "question": "Apakah kamu mengonsumsi alkohol?",
        "options": ["Tidak pernah", "Pernah tapi sudah berhenti", "Kadang-kadang", "Sering / rutin"],
        "scores": [100, 90, 60, 20],
    },
    "Makanan instan": {
        "question": "Seberapa sering kamu makan makanan cepat saji atau instan?",
        "options": ["Jarang sekali", "Kadang-kadang", "Sering", "Hampir setiap hari"],
        "scores": [100, 80, 50, 20],
    },
    "Waktu layar": {
        "question": "Berapa jam per hari kamu menatap layar (HP/komputer/TV) di luar urusan penting?",
        "options": ["<2 jam", "2–4 jam", "5–6 jam", ">6 jam"],
        "scores": [100, 80, 50, 20],
    },

    # --- C. Mental & Sosial ---
    "Stres": {
        "question": "Seberapa sering kamu merasa stres berat, cemas, atau sulit tidur karena pikiran?",
        "options": ["Jarang", "Kadang-kadang", "Cukup sering", "Hampir setiap hari"],
        "scores": [100, 80, 50, 20],
    },
    "Kebahagiaan": {
        "question": "Secara umum, apakah kamu merasa bahagia dan puas dengan hidupmu?",
        "options": ["Ya, sangat", "Cukup bahagia", "Biasa saja", "Tidak bahagia"],
        "scores": [100, 80, 50, 20],
    },
    "Hubungan sosial": {
        "question": "Seberapa sering kamu berinteraksi positif dengan keluarga, teman, atau komunitas?",
        "options": ["Setiap hari", "Beberapa kali seminggu", "Jarang", "Hampir tidak pernah"],
        "scores": [100, 80, 50, 20],
    },
    "Kegiatan spiritual": {
        "question": "Seberapa sering kamu berdoa, beribadah, atau bermeditasi dengan khusyuk?",
        "options": ["Setiap hari", "Beberapa kali seminggu", "Kadang-kadang", "Jarang sekali"],
        "scores": [100, 80, 60, 30],
    },
    "Rasa syukur": {
        "question": "Seberapa sering kamu mensyukuri hal-hal kecil dalam hidup?",
        "options": ["Setiap hari", "Kadang-kadang", "Jarang", "Tidak pernah terpikir"],
        "scores": [100, 80, 50, 20],
    },

    # --- D. Lingkungan & Pencegahan ---
    "Lingkungan": {
        "question": "Bagaimana kondisi lingkungan tempat tinggalmu (kebersihan, polusi, air, sanitasi)?",
        "options": ["Sangat bersih & sehat", "Cukup baik", "Kurang bersih", "Buruk / polusi tinggi"],
        "scores": [100, 80, 50, 20],
    },
    "Pemeriksaan rutin": {
        "question": "Seberapa sering kamu melakukan pemeriksaan kesehatan rutin (tensi, kolesterol, dll)?",
        "options": ["Setahun sekali", "Kadang jika sakit", "Jarang", "Tidak pernah"],
        "scores": [100, 80, 50, 20],
    },
    "Keamanan diri": {
        "question": "Apakah kamu selalu menggunakan sabuk pengaman / helm saat berkendara?",
        "options": ["Selalu", "Sering", "Kadang-kadang", "Tidak pernah"],
        "scores": [100, 80, 50, 20],
    },
}

# ------------------------------
# Pengisian
# ------------------------------
st.markdown("## 📝 Kuis")

answers = {}
for key, q in questions.items():
    answers[key] = st.radio(
        q["question"],
        options=["-- Pilih jawaban --"] + q["options"],
        key=key
    )

# ------------------------------
# Tombol Hasil
# ------------------------------
if st.button("📊 Lihat Hasil"):
    if any(a == "-- Pilih jawaban --" for a in answers.values()):
        st.warning("⚠️ Mohon isi semua pertanyaan sebelum melihat hasil.")
    else:
        scores = []
        total_score = 0
        for key, ans in answers.items():
            idx = questions[key]["options"].index(ans)
            score = questions[key]["scores"][idx]
            scores.append(score)
            total_score += score

        avg_score = total_score / len(questions)
        df = pd.DataFrame({"Kategori": list(questions.keys()), "Skor": scores})

        # Interpretasi hasil
        if avg_score >= 85:
            level = "🟢 Risiko Rendah"
            message = "Gaya hidupmu sangat sehat! Terus pertahankan kebiasaan positif ini."
            life_expectancy = "≈ 80–90 tahun"
        elif avg_score >= 65:
            level = "🟡 Risiko Sedang"
            message = "Cukup baik, tapi masih ada beberapa hal yang bisa kamu perbaiki."
            life_expectancy = "≈ 70–80 tahun"
        else:
            level = "🔴 Risiko Tinggi"
            message = "Beberapa kebiasaan perlu segera diubah agar kesehatan jangka panjang meningkat."
            life_expectancy = "≈ <70 tahun"

        # Hasil utama
        st.success(f"**{level}** — Skor rata-rata: {avg_score:.1f}")
        st.write(message)
        st.markdown(f"📈 **Perkiraan harapan hidup:** {life_expectancy}")
        st.divider()

     

        # Grafik pie
        st.subheader("🧩 Proporsi Kesehatan Keseluruhan")
        fig2, ax2 = plt.subplots()
        ax2.pie(df["Skor"], labels=df["Kategori"], autopct="%1.0f%%", startangle=90, 
                colors=plt.cm.Paired.colors)
        ax2.axis("equal")
        st.pyplot(fig2)

        st.divider()
        st.markdown("💡 *Hasil ini hanya bersifat edukatif. kuis ini berbasis pada prinsip-prinsip ilmiah dari kesehatan masyarakat dan epidemiologi gaya hidup, yang memang berhubungan langsung dengan risiko penyakit kronis dan harapan hidup. Untuk pemeriksaan lebih akurat, konsultasikan dengan tenaga medis profesional.*")
