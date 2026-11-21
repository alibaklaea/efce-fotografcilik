# QR Anı Duvarı — Kurulum (bir kez, ~10 dakika)

Misafirlerin gönderdiği fotoğraflar **Efce'nin kendi Google Drive'ına** kaydedilir.
Bu yüzden kurulum, Efce'nin Google hesabıyla yapılmalıdır.

## 1. Servisi kur
1. Efce'nin Google hesabıyla <https://script.google.com> → **Yeni proje**.
2. Proje adını `Efce QR Anı Duvarı` yapın.
3. `Code.gs` içindekileri silip bu klasördeki `Code.gs` dosyasının tamamını yapıştırın, kaydedin.
4. Üstteki işlev listesinden **kurulum** seçip **Çalıştır**'a basın.
   Google izin isteyecek → hesabı seçin → *Gelişmiş* → *... projesine git (güvenli değil)* → **İzin ver**.
   (Uyarı, betiği Google değil siz yazdığınız için çıkar; Drive'ınızda yalnızca bu klasöre dosya ekler.)
   Drive'da **Efce QR Anı Duvarı** klasörü oluşur.

## 2. Web uygulaması olarak yayınla
1. Sağ üstte **Dağıt → Yeni dağıtım** → tür: **Web uygulaması**.
2. *Şu kullanıcı olarak çalıştır:* **Ben** · *Erişimi olanlar:* **Herkes**.
3. **Dağıt** → verilen `https://script.google.com/macros/s/.../exec` adresini kopyalayın.
4. Bu adresi siteyi yöneten kişiye gönderin; `qr/ayar.js` dosyasındaki `endpoint` alanına yazılacak.

## 3. Her düğün için
1. <https://efcefotografcilik.com.tr/qr/kart.html> → çiftin adını ve tarihi yazın.
2. Ekranda çıkan **düğün kodu** adıyla, Drive'daki *Efce QR Anı Duvarı* klasörünün içinde yeni bir klasör açın
   (ör. `ayse-mehmet-k7p23`). Klasör yoksa yükleme kabul edilmez; bu, yabancıların dosya göndermesini engeller.
3. **Yazdır** → A4'e 4 kart → kesin, masalara koyun.
4. Kartı telefonla okutup bir deneme fotoğrafı gönderin; klasöre düştüğünü kontrol edin.
5. Düğünden sonra klasörü Drive'dan çiftle paylaşın.
6. İşi bitince klasörün adını değiştirin (ör. sonuna `-kapali` ekleyin): yeni yükleme alınmaz.

## Bilinmesi gerekenler
- Ücretsiz Google hesabında 15 GB alan vardır; fotoğraflar telefonda küçültülerek (~1–2 MB) gönderilir.
- Misafirler onay kutusunu işaretlemeden gönderemez (KVKK açısından açık rıza).
- Kodu değiştirdikten sonra (`Code.gs`) **Dağıt → Dağıtımları yönet → Düzenle → Yeni sürüm** ile güncelleyin; adres değişmez.
