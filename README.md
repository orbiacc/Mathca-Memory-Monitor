# 🌍 app.exe Memory Monitor - Multi-Language

Modern, çok dilli bellek izleme aracı. GitHub'dan otomatik dil güncellemeleri alır.

## ✨ Özellikler

- 🌍 **Çok Dilli Destek** - GitHub'dan otomatik dil dosyası indirme
- 💾 **Akıllı Bellek İzleme** - USS (Unique Set Size) ile doğru ölçüm
- 🔄 **Otomatik Yeniden Başlatma** - Sonsuz döngü koruması ile
- 🚀 **Windows Başlangıç Desteği**
- 🎨 **Modern Dark Mode Arayüz**
- 📊 **Canlı Sistem Tepsisi İzleme**
- ⚙️ **Kolay Konfigürasyon**

## 📥 Kurulum

### Gereksinimler
```bash
pip install psutil customtkinter pillow pystray requests
```

### Program Kurulumu
1. `memory_monitor.pyw` dosyasını indirin
2. Gerekli kütüphaneleri yükleyin
3. Programı çalıştırın

## 🌐 Dil Dosyaları Oluşturma

### GitHub Repository Yapısı
```
your-repo/
├── languages/
│   ├── en.json
│   ├── tr.json
│   ├── de.json
│   ├── fr.json
│   ├── es.json
│   └── ...
└── README.md
```

### Dil Dosyası Formatı

Her dil dosyası JSON formatında olmalıdır:

```json
{
  "app_title": "Memory Monitor",
  "running": "Running",
  "not_running": "Not Running",
  "memory_usage": "Memory Usage",
  "configuration": "Configuration",
  "settings": "Settings"
}
```

### Desteklenen Diller

- 🇬🇧 **en** - English
- 🇹🇷 **tr** - Türkçe
- 🇩🇪 **de** - Deutsch
- 🇫🇷 **fr** - Français
- 🇪🇸 **es** - Español
- 🇮🇹 **it** - Italiano
- 🇵🇹 **pt** - Português
- 🇷🇺 **ru** - Русский
- 🇨🇳 **zh** - 中文
- 🇯🇵 **ja** - 日本語
- 🇰🇷 **ko** - 한국어

## ⚙️ Konfigürasyon

### memory_monitor.pyw İçinde Ayarlanması Gerekenler

**ÖNEMLİ:** Programı kullanmadan önce GitHub URL'inizi güncelleyin:

```python
# GitHub dil dosyaları URL'i (KENDI REPO'NUZU KULLANIN!)
GITHUB_LANGUAGES_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/languages/"
```

**Örnek:**
```python
# Doğru kullanım
GITHUB_LANGUAGES_URL = "https://raw.githubusercontent.com/johndoe/memory-monitor-langs/main/languages/"
```

### Dil Dosyası API URL'i

Program ayrıca GitHub API'den dil listesini çeker:

```python
url = "https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/contents/languages"
```

Bunu da güncelleyin:
```python
url = "https://api.github.com/repos/johndoe/memory-monitor-langs/contents/languages"
```

## 📝 Yeni Dil Ekleme

### 1. Dil Dosyası Oluşturun

`languages/` klasöründe yeni bir JSON dosyası oluşturun (örn: `de.json` Almanca için):

```json
{
  "app_title": "app.exe Speicher-Monitor",
  "memory_monitor": "Speicher-Monitor",
  "running": "Läuft",
  "not_running": "Läuft nicht",
  "restart_blocked": "Neustart blockiert",
  "status": "Status",
  "memory_usage": "Speichernutzung",
  "limit": "Limit",
  "configuration": "Konfiguration",
  "settings": "Einstellungen",
  "hide": "Verstecken",
  "close": "Schließen",
  "save_apply": "Speichern & Anwenden",
  "on": "An",
  "off": "Aus",
  "enabled": "Aktiviert",
  "disabled": "Deaktiviert"
}
```

### 2. Bayrak Ekojisi Ekleyin (Opsiyonel)

`memory_monitor.pyw` içinde `lang_names` dictionary'sine ekleyin:

```python
lang_names = {
    "en": "🇬🇧 English",
    "tr": "🇹🇷 Türkçe",
    "de": "🇩🇪 Deutsch",  # Yeni eklenen
    # ... diğer diller
}
```

### 3. GitHub'a Push Edin

```bash
git add languages/de.json
git commit -m "Add German language support"
git push origin main
```

Program otomatik olarak yeni dili algılayacak ve kullanıcılara sunacaktır!

## 🔧 Kullanım

### İlk Çalıştırma

1. Programı çalıştırın
2. Sistem tepsisinde RAM ikonu görünecek
3. İkona çift tıklayarak ana pencereyi açın

### Ayarlar

**Konfigürasyon Penceresi:**
- Bellek limiti ayarlama (100 MB - 32 GB)
- Güncelleme aralığı (0.5 - 60 saniye)

**Ayarlar Penceresi:**
- 🌍 Dil seçimi (GitHub'dan otomatik indirilir)
- 🔄 Otomatik yeniden başlatma
- 🚀 Windows başlangıcı

### Sistem Tepsisi

- **Yeşil RAM:** Normal kullanım (<%75)
- **Sarı RAM:** Yüksek kullanım (75-90%)
- **Kırmızı RAM:** Kritik kullanım (>90%)
- **Gri RAM:** Program çalışmıyor

## 🛡️ Güvenlik Özellikleri

- ✅ Tek instance garantisi (Mutex kilitleme)
- ✅ Sonsuz döngü koruması (60 saniyede max 3 restart)
- ✅ Güvenli process termination
- ✅ Otomatik bloke sistemi

## 📊 Teknik Detaylar

### Bellek Ölçümü

Program **USS (Unique Set Size)** kullanır - Windows Görev Yöneticisi ile %100 uyumlu:
- Sadece process'e özel bellek
- Paylaşımlı DLL'ler dahil değil
- En doğru RAM kullanım ölçümü

### Dosya Yolları

- Config: `%USERPROFILE%/app_memory_monitor_config.json`
- Dil dosyaları: `%USERPROFILE%/.app_memory_monitor/languages/`

## 🤝 Katkıda Bulunma

Yeni dil eklemeleri için:

1. Fork yapın
2. Yeni dil dosyası ekleyin (`languages/xx.json`)
3. Pull request gönderin

## 📜 Lisans

MIT License - Özgürce kullanabilir ve değiştirebilirsiniz.

## 🆘 Sorun Giderme

### "Dil dosyası indirilemedi"

- İnternet bağlantınızı kontrol edin
- GitHub URL'inizi doğrulayın
- Repository'nin public olduğundan emin olun

### "Program zaten çalışıyor"

- Sistem tepsisine bakın
- Task Manager'dan eski process'i kapatın

### "Otomatik başlatma bloke edildi"

- RAM limitinizi artırın (Konfigürasyon → Bellek Limiti)
- app.exe'nin normal çalışması için daha fazla RAM gerekiyor

## 📞 İletişim

Sorunlar için GitHub Issues kullanın.

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**
