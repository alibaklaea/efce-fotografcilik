/* ===== AYARLAR — telefon, Instagram ve Google yorum linki buradan değişir ===== */
const AYAR = {
  telefon:   "905070030406",          // başında 90, boşluksuz
  telGoster: "0 (507) 003 04 06",     // sitede görünen hâli
  instagram: "efcephotography",       // @ olmadan kullanıcı adı
  harita:    "https://maps.app.goo.gl/XtkhT6yEuW76n4cDA" // Google Haritalar kaydı (yorum da buradan yazılır)
};
/* ============================================================================== */

const wa = m => `https://wa.me/${AYAR.telefon}?text=${encodeURIComponent(m)}`;
const $$ = s => [...document.querySelectorAll(s)];
const ext = a => { a.target = "_blank"; a.rel = "noopener"; };

$$('[data-wa]').forEach(a => { a.href = wa(a.dataset.wa); ext(a); });
$$('[data-ig]').forEach(a => { a.href = `https://instagram.com/${AYAR.instagram}`; ext(a); });
$$('[data-ig-text]').forEach(a => a.textContent = '@' + AYAR.instagram);
$$('[data-tel]').forEach(a => { a.href = 'tel:+' + AYAR.telefon; a.textContent = AYAR.telGoster; });
$$('[data-harita]').forEach(a => { a.href = AYAR.harita; ext(a); });
$$('.yil').forEach(e => e.textContent = new Date().getFullYear());

// menü
const nav = document.getElementById('nav'), links = document.getElementById('links');
if (nav) addEventListener('scroll', () => nav.classList.toggle('solid', scrollY > 60), { passive: true });
if (links) {
  document.getElementById('burger').onclick = () => links.classList.toggle('open');
  links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));
}

// açılış fotoğrafları
const slides = $$('.slide'), dots = document.getElementById('dots');
if (slides.length > 1 && dots) {
  let cur = 0, timer;
  slides.forEach((_, i) => { const b = document.createElement('button'); b.setAttribute('aria-label', `Fotoğraf ${i + 1}`); b.onclick = () => go(i); dots.appendChild(b); });
  function go(i) {
    slides[cur].classList.remove('on'); dots.children[cur].classList.remove('on');
    cur = (i + slides.length) % slides.length;
    const s = slides[cur]; s.style.animation = 'none'; s.offsetHeight; s.style.animation = '';
    s.classList.add('on'); dots.children[cur].classList.add('on');
    clearInterval(timer); timer = setInterval(() => go(cur + 1), 6500);
  }
  go(0);
}

// galeri filtreleri
const figs = $$('#grid figure');
$$('#filters button').forEach(b => b.onclick = () => {
  $$('#filters button').forEach(x => x.classList.remove('on')); b.classList.add('on');
  figs.forEach(f => f.classList.toggle('hide', b.dataset.f !== 'hepsi' && f.dataset.c !== b.dataset.f));
});

// PhotoSwipe galeri (kaydırma + yakınlaştırma)
const kok = document.querySelector('script[src*="site.js"]').src.replace(/site\.js.*$/, '');
if (document.querySelector('.pswp-gallery')) {
  const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = kok + 'vendor/photoswipe.css'; document.head.appendChild(css);
  import(kok + 'vendor/photoswipe-lightbox.esm.min.js').then(({ default: PhotoSwipeLightbox }) => {
    const lightbox = new PhotoSwipeLightbox({
      gallery: '.pswp-gallery', children: 'figure:not(.hide) a',
      pswpModule: () => import(kok + 'vendor/photoswipe.esm.min.js'),
      bgOpacity: .96, showHideAnimationType: 'zoom',
      closeTitle: 'Kapat', zoomTitle: 'Yakınlaştır', arrowPrevTitle: 'Önceki', arrowNextTitle: 'Sonraki', errorMsg: 'Fotoğraf yüklenemedi'
    });
    lightbox.on('uiRegister', () => {
      lightbox.pswp.ui.registerElement({
        name: 'caption', order: 9, isButton: false, appendTo: 'root',
        onInit: (el, pswp) => pswp.on('change', () => {
          const c = pswp.currSlide.data.element?.closest('figure')?.querySelector('figcaption');
          el.textContent = c ? c.textContent : '';
        })
      });
    });
    lightbox.init();
  });
}

// form → WhatsApp
const form = document.getElementById('form');
if (form) form.onsubmit = e => {
  e.preventDefault(); const d = new FormData(form);
  const t = d.get('tarih') ? new Date(d.get('tarih')).toLocaleDateString('tr-TR') : 'belirtilmedi';
  const m = `Merhaba, ben ${d.get('ad')}.\nÇekim türü: ${d.get('tur')}\nTarih: ${t}\nTelefon: ${d.get('tel') || '-'}\n${d.get('mesaj') || ''}`;
  window.open(wa(m), '_blank');
};

// kaydırınca beliren bölümler
const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }), { threshold: .12 });
$$('.rv').forEach((el, i) => { el.style.transitionDelay = (el.closest('.place-list,.steps,.qr-steps') ? (i % 4) * .08 : 0) + 's'; io.observe(el); });
