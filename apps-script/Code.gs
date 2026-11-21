/**
 * Efce Fotoğrafçılık — QR Anı Duvarı yükleme servisi (Google Apps Script)
 * Misafir sayfasından (qr/yukle.html) gelen fotoğrafları Google Drive'da
 *   "Efce QR Anı Duvarı / <etkinlik-kodu>"
 * klasörüne kaydeder. Klasör önceden açılmamışsa yükleme REDDEDİLİR
 * (böylece bağlantıyı tahmin eden yabancılar Drive'a dosya bırakamaz).
 * Kurulum: KURULUM.md
 */
const KOK_KLASOR = 'Efce QR Anı Duvarı';
const MAKS_BAYT = 15 * 1024 * 1024;
const TURLER = { 'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp', 'image/heic': 'heic', 'image/heif': 'heif' };

function doPost(e) {
  try {
    const v = JSON.parse(e.postData.contents);
    const kod = String(v.etkinlik || '').toLowerCase().replace(/[^a-z0-9-]/g, '');
    if (!kod || kod === 'ornek') return cevap_({ ok: false, hata: 'kod' });

    const kokler = DriveApp.getFoldersByName(KOK_KLASOR);
    if (!kokler.hasNext()) return cevap_({ ok: false, hata: 'kok-klasor-yok' });
    const etkinlikler = kokler.next().getFoldersByName(kod);
    if (!etkinlikler.hasNext()) return cevap_({ ok: false, hata: 'etkinlik-yok' });
    const klasor = etkinlikler.next();

    const uzanti = TURLER[v.mime];
    if (!uzanti) return cevap_({ ok: false, hata: 'tur' });
    const bayt = Utilities.base64Decode(String(v.veri || ''));
    if (!bayt.length || bayt.length > MAKS_BAYT) return cevap_({ ok: false, hata: 'boyut' });

    const ad = String(v.ad || 'Misafir').replace(/[^0-9A-Za-zÇĞİÖŞÜçğıöşü .\-]/g, '').trim().slice(0, 40) || 'Misafir';
    const zaman = Utilities.formatDate(new Date(), 'Europe/Istanbul', 'yyyyMMdd-HHmmss');
    const dosyaAdi = `${zaman}_${ad}_${Math.random().toString(36).slice(2, 7)}.${uzanti}`;
    klasor.createFile(Utilities.newBlob(bayt, v.mime, dosyaAdi));
    return cevap_({ ok: true });
  } catch (err) {
    return cevap_({ ok: false, hata: String(err) });
  }
}

/** Tarayıcıdan adres açıldığında servisin çalıştığını gösterir. */
function doGet() {
  return cevap_({ ok: true, servis: 'Efce QR Anı Duvarı' });
}

/** İlk kurulumda bir kez çalıştırın: kök klasörü oluşturur ve Drive izni ister. */
function kurulum() {
  const it = DriveApp.getFoldersByName(KOK_KLASOR);
  const kok = it.hasNext() ? it.next() : DriveApp.createFolder(KOK_KLASOR);
  Logger.log('Kök klasör hazır: ' + kok.getUrl());
}

function cevap_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
