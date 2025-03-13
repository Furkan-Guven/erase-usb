# 🔥 USB Secure Erase Tool

Bu proje, **Windows ve macOS** için geliştirilmiş bir **güvenli USB sıfırlama** aracıdır.**random (rastgele veri yazma)** ve **zeros (sıfırlarla doldurma)** yöntemleri ile **USB flash belleklerdeki verileri güvenli bir şekilde siler** ve FAT32/NTFS olarak yeniden biçimlendirme imkanı sunar.

## 🚀 Özellikler
- **Bağlı USB sürücülerini listeleme**
- **Güvenli silme yöntemleri:**
  - 🔹 **Zeros Method** (Tüm hücreleri `0x00` ile doldurur)
  - 🔹 **Random Method** (Tüm hücrelere rastgele veri yazar)
  - 🔹 **Hybrid Method** (Önce rastgele veri, ardından sıfırlarla doldurma)
- **FAT32 veya NTFS olarak biçimlendirme**
- **Kullanıcı dostu arayüz (Tkinter)**
- **İlerleme çubuğu ile anlık durum göstergesi**
- **İşlem süresi hesaplama ve raporlama**

---

## ❓ Neden Bu Yöntemler?

### 🔹 **Zeros Method (Sıfırlarla Doldurma)**
USB bellekteki her hücreyi `0x00` ile doldurur. Çoğu kullanıcı için yeterlidir ancak bazı veri kurtarma tekniklerine karşı zayıf olabilir.

### 🔹 **Random Method (Rastgele Veri Yazma)**
Hücreleri rastgele `0x00 - 0xFF` arasında değerlerle doldurur. Verinin geri getirilmesini zorlaştırır.

### 🔹 **Hybrid Method (İkili Yöntem)**
İlk olarak **rastgele veri**, ardından **sıfırlarla** doldurma işlemi yapar. Bu, NAND flash yapısına bağlı olarak en güvenli yöntemdir.

### ⚠️ **Gutmann Yöntemi Neden Yok?**
Gutmann yöntemi **HDD’ler için geliştirilmiştir** ve modern NAND flash’lar için gereksizdir. USB’ler **wear leveling (aşınma dengeleme) algoritması** kullandığından, 35 geçişlik Gutmann işlemi NAND’da etkili değildir.

---

## ⏳ İşlem Süresi Hesaplama
**Teorik süre hesaplama formülü:**
```
Süre (s) = (USB Kapasitesi (MB) / USB Yazma Hızı (MB/s)) * Katman Sayısı
```

📌 **Örnek:**
- **3GB USB Bellek** (3000 MB)
- **Ortalama yazma hızı**: **10 MB/s**
- **Tek katmanlı yazım (zeros/random)**
```
Süre = (3000 / 10) * 1 = 300 saniye (~5 dakika)
```
**Hybrid Method** için süre **2 katına çıkacaktır.**

---

## 🛠 Kurulum ve Kullanım

### 🍎 macOS için `.app` oluşturma
```sh
pyinstaller --onefile --windowed --name "USB_Eraser" usb_eraser_macos.py
```

### 🖥 Windows için `.exe` oluşturma
```sh
pip install -r requirements.txt
pyinstaller --onefile --windowed --name "USB_Eraser" usb_eraser_windows.py
```

---

## 🤝 Katkıda Bulunma

Eğer projeye katkı sağlamak isterseniz:
- 🍴 **Fork yapın**
- 🌱 **Kendi branch’inizde geliştirme yapın**
- 🚀 **Pull request gönderin**

Her türlü geri bildiriminizi bekliyoruz! ✨
