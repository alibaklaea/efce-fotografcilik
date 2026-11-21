"""Efce Fotoğrafçılık — mekân sayfalarını, ana sayfa mekân kartlarını ve sitemap.xml'i üretir.
Kullanım:  python yap.py
Yeni mekân eklemek için MEKANLAR listesine bir sözlük ekleyip betiği çalıştırın."""
import json, re, html, os
from datetime import date

SITE = "https://efcefotografcilik.com.tr"
DIMS = json.load(open("assets/dims.json"))

MEKANLAR = [
 dict(slug="silifke-kalesi", ad="Silifke Kalesi", kisa="Şehir merkezi", foto="p6",
  kart="Tepeden Göksu ovasına bakan taş surlar; tarihi ve görkemli kareler.", zaman="İkindi & gün batımı",
  baslik="Silifke Kalesi'nde Dış Çekim", konum="Silifke şehir merkezi, kale tepesi",
  ozet="Şehrin üzerinde yükselen ortaçağ kalesi: taş surlar, burçlar ve aşağıda uzanan Göksu ovası.",
  neden=["Taş surlar ve kemerler, gelinliğin beyazıyla güçlü bir kontrast oluşturur.",
         "Tepeden şehir ve Göksu ovası manzarası, geniş açılı kareler için eşsiz bir arka plan sunar.",
         "Stüdyomuza yakın olduğu için stüdyo çekimiyle aynı güne kolayca sığar."],
  saatNot="Akşamüstü yumuşayan ışık taşın dokusunu ortaya çıkarır; gün batımından sonra şehir ışıklarıyla devam edebiliriz.",
  ipucu=["Taş zeminde rahat yürüyebileceğiniz yedek bir ayakkabı getirin.",
         "Tepe rüzgârlı olabilir; duvak ve saç için toka bulundurun.",
         "Yaz aylarında öğle sıcağından kaçınıp akşamüstünü tercih ediyoruz."],
  bilgi="Kale ziyarete açık tarihi bir alandır; ziyaret saatleri ve restorasyon çalışmaları nedeniyle erişim değişebilir. Çekim gününden önce durumu birlikte kontrol ediyoruz."),
 dict(slug="taskopru-goksu", ad="Taşköprü & Göksu", kisa="Şehir merkezi", foto="p2",
  kart="Göksu Nehri üzerindeki tarihi köprü ve nehir kıyısı; sakin, romantik tonlar.", zaman="Sabah erken",
  baslik="Taşköprü ve Göksu Kıyısında Dış Çekim", konum="Silifke şehir merkezi",
  ozet="Göksu Nehri üzerinde, kökeni Roma dönemine uzanan tarihi Taşköprü ve yemyeşil nehir kıyısı.",
  neden=["Köprünün taş kemerleri ve nehrin akışı zamansız, romantik bir çerçeve sunar.",
         "Nehir kıyısındaki yeşillik yumuşak ve doğal tonlar verir.",
         "Şehrin içinde olduğu için kısa sürede ulaşılır; yürüyüş tarzı doğal kareler için ideal."],
  saatNot="Sabah saatlerinde hem ışık yumuşak hem de çevre daha sakin olur.",
  ipucu=["Köprü trafiğe açık olabildiği için kareleri kıyıdan ve köprü başlarından kuruyoruz.",
         "Nehir kenarında zemin kaygan olabilir; düz tabanlı ayakkabı faydalı olur.",
         "Akşam serinliği için ince bir şal bulundurun."],
  bilgi="Şehir içinde, herkese açık bir alandır; günün yoğun saatlerinde yaya ve araç trafiği olabilir."),
 dict(slug="goksu-deltasi", ad="Delta & Sazlıklar", kisa="Göksu Deltası", foto="p2",
  kart="Uçsuz sazlıklar, lagünler ve kuş sesleri; doğal ve sinematik geniş açılar.", zaman="Altın saat",
  baslik="Göksu Deltası'nda Dış Çekim", konum="Silifke – Taşucu arası, Göksu'nun denize döküldüğü alan",
  ozet="Sazlıklar, lagünler ve kumullarla Türkiye'nin önemli sulak alanlarından biri.",
  neden=["Uçsuz sazlıklar ve su yüzeyi, sinematik geniş planlar için doğal bir dekor oluşturur.",
         "Rüzgârda dalgalanan sazlar gelinlikte hareketli ve doğal kareler sağlar.",
         "Kalabalıktan uzak, rahat ve sakin bir çekim ortamı sunar."],
  saatNot="Düz ve açık arazide güneşin alçaldığı saatler en etkileyici siluetleri verir.",
  ipucu=["Sinek ve sivrisineğe karşı koruyucu sprey getirin.",
         "Kumlu ve çamurlu zeminler için yedek ayakkabı şart.",
         "Uzun kuyruklu gelinlikler için kuru bir alan seçip kısa yürüyüşler planlıyoruz."],
  bilgi="Göksu Deltası koruma altındaki bir doğal alandır. Kuşlara ve bitki örtüsüne zarar vermeden, izin verilen yollarda ve alanlarda çekim yapıyoruz."),
 dict(slug="tasucu", ad="Taşucu Sahili", kisa="Taşucu", foto="p3",
  kart="İskele, tekneler ve deniz; gün batımında altın rengi bir arka plan.", zaman="Gün batımı",
  baslik="Taşucu'nda Dış Çekim", konum="Taşucu, Silifke",
  ozet="Silifke'nin liman kasabası: iskele, tekneler, sahil ve deniz manzarası.",
  neden=["İskele ve tekneler, Akdeniz'e özgü canlı ve renkli kareler sağlar.",
         "Deniz ve gökyüzü gün batımına doğru altın tonlara bürünür; siluet kareler için ideal.",
         "Sahil boyunca kısa mesafelerde farklı arka planlar bulunur."],
  saatNot="Gün batımına yakın saatlerde deniz ve gökyüzü sıcak tonlara bürünür.",
  ipucu=["Deniz kenarında rüzgâr olabilir; duvak için toka getirin.",
         "Islanmayı göze alırsanız sığ suda çok özel kareler çıkar; trash the dress için de uygun.",
         "Liman bölgesinde güvenlik kurallarına uyarak çekim noktalarını önceden seçiyoruz."],
  bilgi="Liman ve iskele alanlarında bazı bölgelere giriş kısıtlı olabilir; herkese açık sahil ve iskele noktalarını kullanıyoruz."),
 dict(slug="kizkalesi", ad="Kızkalesi", kisa="Kızkalesi", foto="p5",
  kart="Denizin ortasındaki efsanevi kale; masalsı bir Akdeniz kartpostalı.", zaman="Gün doğumu",
  baslik="Kızkalesi'nde Dış Çekim", konum="Kızkalesi, Erdemli – Silifke'ye kısa bir yolculuk",
  ozet="Denizin ortasındaki efsanevi Kız Kalesi ve karşısındaki Korykos kara kalesi; Akdeniz'in en tanınan manzaralarından.",
  neden=["Denizin içindeki kale, arka planda masalsı bir siluet oluşturur.",
         "Kumsal ve berrak deniz; hem romantik hem eğlenceli kareler.",
         "Kara kalesinin taş surlarıyla aynı gün iki farklı atmosfer yakalanır."],
  saatNot="Yaz aylarında plaj kalabalık olabildiği için sabah erken saatleri öneriyoruz.",
  ipucu=["Yaz sezonunda sabahın erken saatleri hem serin hem sakin geçer.",
         "Kumsalda çekim için gelinlik eteğini koruyacak şekilde plan yapıyoruz.",
         "Denizdeki kaleye tekneyle geçiş mevsime ve hava durumuna bağlıdır; isterseniz birlikte planlarız."],
  bilgi="Korykos kara kalesi bir ören yeridir; profesyonel çekim için müze müdürlüğü izni gerekebilir. Planlarken birlikte kontrol ediyoruz."),
 dict(slug="narlikuyu", ad="Narlıkuyu Koyu", kisa="Narlıkuyu", foto="p7",
  kart="Turkuaz su, kayalıklar ve balıkçı kasabası dokusu.", zaman="Öğleden sonra",
  baslik="Narlıkuyu Koyu'nda Dış Çekim", konum="Narlıkuyu, Silifke",
  ozet="Turkuaz suyu, kayalıkları ve küçük balıkçı limanıyla sakin bir Akdeniz koyu.",
  neden=["Kayalıklar ve berrak su, gelinliğin beyazıyla çarpıcı bir kontrast verir.",
         "Balıkçı tekneleri ve liman dokusu doğal, samimi kareler sağlar.",
         "Cennet–Cehennem obruklarına çok yakın; aynı gün iki mekân birleştirilebilir."],
  saatNot="Suyun turkuaz rengi güneş yükseldiğinde en canlı hâlini alır; sert ışığı yumuşatmak için gölgeli noktaları kullanıyoruz.",
  ipucu=["Kayalıklarda kaymayan tabanlı ayakkabı şart.",
         "Deniz kenarında makyajı sabitleyen sprey işinize yarar.",
         "Çekim sonrası koydaki restoranlarda küçük bir kutlama güzel bir kapanış olur."],
  bilgi="Koy herkese açıktır; restoran ve özel işletme alanlarında çekim için işletmeden izin alıyoruz."),
 dict(slug="cennet-cehennem", ad="Cennet–Cehennem", kisa="Narlıkuyu yakını", foto="p6",
  kart="Dev obruklar ve yeşil doğa; sıra dışı, dramatik kareler.", zaman="Sabah",
  baslik="Cennet–Cehennem Obruklarında Dış Çekim", konum="Narlıkuyu yakını, Silifke",
  ozet="Yerin derinliklerine inen dev obruklar, yemyeşil bitki örtüsü ve dipte tarihi bir şapel.",
  neden=["Dev obruğun derinliği ve yeşil duvarlar sıra dışı, dramatik bir sahne kurar.",
         "Merdivenlerle inilen patika boyunca farklı ışık ve doku katmanları bulunur.",
         "Sıradan dış çekimlerden ayrılmak isteyen çiftler için unutulmaz bir seçenek."],
  saatNot="Obruğun içine ışık güneş yükseldikçe girer; sabah saatleri hem serin hem daha sakindir.",
  ipucu=["Uzun bir merdiven inişi ve çıkışı var; rahat ayakkabı ve su getirin.",
         "Kuyruklu gelinlik yerine hafif, kısa etekli ikinci bir kıyafet düşünebilirsiniz.",
         "Obruk içi serin ve nemli olabilir; makyaj ve saç için buna göre hazırlanıyoruz."],
  bilgi="Cennet–Cehennem ücretli bir ören yeridir; profesyonel çekim için müze müdürlüğü izni gerekebilir. Planlarken birlikte kontrol ediyoruz."),
 dict(slug="uzuncaburc", ad="Antik Kent", kisa="Uzuncaburç", foto="p1",
  kart="Yükselen antik sütunlar ve tapınak kalıntıları; zamansız, epik bir atmosfer.", zaman="Altın saat",
  baslik="Uzuncaburç Antik Kenti'nde Dış Çekim", konum="Uzuncaburç, Silifke'nin kuzeyi",
  ozet="Antik Diokaisareia: Zeus Olbios Tapınağı'nın yükselen sütunları, tiyatro ve kent kapısı.",
  neden=["Yükselen antik sütunlar epik ve zamansız kareler sunar.",
         "Yayla havası sayesinde yaz aylarında sahile göre daha serin bir çekim.",
         "Taş ve gökyüzünün sade uyumu gelinliği öne çıkarır."],
  saatNot="Akşamüstü ışığı sütunlar arasında uzun gölgeler ve sıcak tonlar oluşturur.",
  ipucu=["Yol biraz uzun ve virajlı; çekimi yarım gün olarak planlıyoruz.",
         "Taş zemin için rahat ayakkabı getirin.",
         "Yayla akşamları serinleyebilir; ince bir ceket bulundurun."],
  bilgi="Uzuncaburç bir ören yeridir; profesyonel çekim için müze müdürlüğü izni gerekebilir. Planlarken birlikte kontrol ediyoruz."),
]

e = lambda s: html.escape(s, quote=True)
adi = lambda m: "Uzuncaburç" if m["ad"] == "Antik Kent" else m["ad"]

def srcset(p, kok):
    return f'{kok}img/{p}-800.webp 800w, {kok}img/{p}-1600.webp 1600w'

NAV = """<nav id="nav" class="solid">
  <div class="wrap">
    <a href="../" class="logo" aria-label="Efce Fotoğrafçılık ana sayfa"><b>EFCE</b><small>Fotoğrafçılık</small></a>
    <div class="links" id="links">
      <a href="../#hizmetler">Hizmetler</a>
      <a href="../#galeri">Galeri</a>
      <a href="../#mekanlar">Mekânlar</a>
      <a href="../#qr">QR Anı Duvarı</a>
      <a href="../#iletisim">İletişim</a>
    </div>
    <a class="btn nav-cta" data-wa="Merhaba, çekim tarihi sormak istiyorum." href="#">Tarih Sor</a>
    <button class="burger" id="burger" aria-label="Menü"><svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" fill="none"><path d="M3 7h18M3 12h18M3 17h18"/></svg></button>
  </div>
</nav>"""

FOOT = """<footer>
  <div class="wrap">
    <a href="../" class="logo"><b>EFCE</b><small>Fotoğrafçılık</small></a>
    <p style="margin-bottom:10px">Göksu Mah. Veli Gürten Bozbey Cad. Kızılay İşhanı No:3/D, Silifke / Mersin · <a href="#" data-tel></a></p>
    <p>© <span class="yil"></span> Efce Fotoğrafçılık · Tüm fotoğrafların hakları saklıdır.</p>
  </div>
</footer>
<a class="wa" data-wa="Merhaba, dış çekim hakkında bilgi almak istiyorum." href="#" aria-label="WhatsApp ile yazın"><svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Z"/></svg></a>
<script src="../assets/site.js" defer></script>"""

def sayfa(m):
    url = f"{SITE}/dis-cekim/{m['slug']}.html"
    digerleri = "".join(f'<a href="{o["slug"]}.html">{e(adi(o))}</a>' for o in MEKANLAR if o is not m)
    ornek = [p for p in ("p5","p3","p8","p9","p1","p7") if p != m["foto"]][:3]
    ornekHTML = "".join(
        f'<figure><a href="../img/{p}-1600.webp" data-pswp-width="{DIMS[p][0]}" data-pswp-height="{DIMS[p][1]}"><img src="../img/{p}-800.webp" srcset="{srcset(p,"../")}" sizes="(max-width:700px) 100vw, 33vw" alt="Efce Fotoğrafçılık örnek çalışma" loading="lazy"></a></figure>'
        for p in ornek)
    ld = {"@context":"https://schema.org","@graph":[
        {"@type":"Service","name":m["baslik"],"serviceType":"Dış çekim / düğün fotoğrafçılığı","areaServed":m["konum"],
         "provider":{"@type":"ProfessionalService","name":"Efce Fotoğrafçılık","telephone":"+905070030406","url":SITE,
           "address":{"@type":"PostalAddress","streetAddress":"Göksu Mah. Veli Gürten Bozbey Cad. Kızılay İşhanı No:3/D","postalCode":"33960","addressLocality":"Silifke","addressRegion":"Mersin","addressCountry":"TR"}}},
        {"@type":"BreadcrumbList","itemListElement":[
         {"@type":"ListItem","position":1,"name":"Ana sayfa","item":SITE+"/"},
         {"@type":"ListItem","position":2,"name":"Dış çekim mekânları","item":SITE+"/#mekanlar"},
         {"@type":"ListItem","position":3,"name":m["baslik"],"item":url}]}]}
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(m['baslik'])} · Efce Fotoğrafçılık Silifke</title>
<meta name="description" content="{e(m['ozet'])} {e(adi(m))} dış çekim ve düğün fotoğrafları için en iyi saat, ipuçları ve bilinmesi gerekenler.">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(m['baslik'])} · Efce Fotoğrafçılık">
<meta property="og:description" content="{e(m['ozet'])}">
<meta property="og:image" content="{SITE}/img/{m['foto']}.jpg">
<meta property="og:type" content="article">
<meta name="theme-color" content="#14110f">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='%2314110f'/><circle cx='32' cy='32' r='15' fill='none' stroke='%23c9a46a' stroke-width='4'/><circle cx='32' cy='32' r='5' fill='%23c9a46a'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{NAV}
<header class="page-hero" style="background-image:linear-gradient(90deg,rgba(20,17,15,.85),rgba(20,17,15,.35)),url(../img/{m['foto']}-1600.webp)">
  <div class="wrap">
    <div class="crumb" role="navigation" aria-label="Konum"><a href="../">Ana sayfa</a> / <a href="../#mekanlar">Mekânlar</a> / <span>{e(adi(m))}</span></div>
    <span class="eyebrow">{e(m['konum'])}</span>
    <h1>{e(m['baslik'])}</h1>
    <p class="lead">{e(m['ozet'])}</p>
    <div class="hero-btns"><a class="btn" data-wa="Merhaba, {e(adi(m))} için dış çekim tarihi sormak istiyorum." href="#">Bu mekân için tarih sor</a></div>
    <p class="photo-note">Görsel: Efce Fotoğrafçılık örnek çalışma</p>
  </div>
</header>

<section class="mekan-detay">
  <div class="wrap md-grid">
    <div class="rv">
      <span class="eyebrow">Neden burada?</span>
      <h2>Bu mekânı <em>özel</em> kılanlar</h2>
      <ul class="tick">{li(m['neden'])}</ul>
    </div>
    <aside class="rv">
      <div class="when-box"><small>En iyi saat</small><b>{e(m['zaman'])}</b><p>{e(m['saatNot'])}</p></div>
      <div class="info-box"><small>Bilinmesi gerekenler</small><p>{e(m['bilgi'])}</p></div>
    </aside>
  </div>
</section>

<section class="mekan-ipucu">
  <div class="wrap rv">
    <span class="eyebrow">Çekim ipuçları</span>
    <h2>Gün gelmeden <em>bilmeniz</em> gerekenler</h2>
    <ol class="tips">{li(m['ipucu'])}</ol>
  </div>
</section>

<section class="mekan-ornek">
  <div class="wrap">
    <div class="sec-head rv"><div><span class="eyebrow">Portfolyo</span><h2>Örnek <em>çalışmalarımız</em></h2></div><p class="lead">Farklı mekânlardaki çekimlerimizden bir seçki. Tamamı için <a href="../#galeri" style="color:var(--gold2);border-bottom:1px solid">galeriye</a> göz atın.</p></div>
    <div class="grid three pswp-gallery">{ornekHTML}</div>
  </div>
</section>

<section class="mekan-cta">
  <div class="wrap rv">
    <h2>Hikâyenizi <em>burada</em> yazalım.</h2>
    <p class="lead">Tarihinizi yazın; ışığa, mevsime ve sizin tarzınıza göre en uygun planı birlikte kuralım.</p>
    <div class="hero-btns" style="justify-content:center"><a class="btn" data-wa="Merhaba, {e(adi(m))} için dış çekim planlamak istiyorum." href="#">WhatsApp'tan Yazın</a><a class="btn ghost" href="#" data-tel></a></div>
    <div class="other"><small>Diğer mekânlar</small><div>{digerleri}</div></div>
  </div>
</section>
{FOOT}
</body>
</html>
"""

def kartlar():
    return "\n".join(
        f'      <a class="place rv" href="dis-cekim/{m["slug"]}.html"><span class="km">{e(m["kisa"])}</span><h3>{e(m["ad"])}</h3><p>{e(m["kart"])}</p><span class="when">{e(m["zaman"])}</span><span class="more">Mekânı incele →</span></a>'
        for m in MEKANLAR)

os.makedirs("dis-cekim", exist_ok=True)
for m in MEKANLAR:
    open(f"dis-cekim/{m['slug']}.html", "w", encoding="utf8").write(sayfa(m))

ix = open("index.html", encoding="utf8").read()
ix = re.sub(r'(<div class="place-list">)(.*?)(\n    </div>)', lambda r: r.group(1) + "\n" + kartlar() + r.group(3), ix, count=1, flags=re.S)
open("index.html", "w", encoding="utf8").write(ix)

bugun = date.today().isoformat()
urls = [SITE + "/"] + [f"{SITE}/dis-cekim/{m['slug']}.html" for m in MEKANLAR]
open("sitemap.xml", "w", encoding="utf8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{u}</loc><lastmod>{bugun}</lastmod></url>\n" for u in urls) + "</urlset>\n")
open("robots.txt", "w", encoding="utf8").write(f"User-agent: *\nAllow: /\nDisallow: /qr/kart.html\nSitemap: {SITE}/sitemap.xml\n")
print(f"{len(MEKANLAR)} mekân sayfası, ana sayfa kartları, sitemap.xml ve robots.txt üretildi.")
