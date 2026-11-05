(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const touch = matchMedia('(hover: none)').matches;

  /* ---------- Navbar: scrolled state, sliding indicator, active section ---------- */
  const nav = $('#nav'), callbar = $('#callbar'), contact = $('#kontakt');
  const links = $$('#navLinks a'), indicator = $('.nav__indicator');
  let active = links.find(l => l.getAttribute('aria-current') === 'page') || null;
  let nearContact = false;
  const onScroll = () => {
    nav.classList.toggle('is-scrolled', scrollY > 8);
    if (callbar) callbar.classList.toggle('is-visible', scrollY > innerHeight * 0.6 && !nearContact);
  };
  const placeIndicator = a => {
    if (!indicator) return;
    if (!a) { indicator.style.opacity = 0; return; }
    const r = a.getBoundingClientRect(), p = indicator.parentElement.getBoundingClientRect();
    indicator.style.width = r.width + 'px';
    indicator.style.transform = `translateX(${r.left - p.left}px)`;
    indicator.style.opacity = 1;
  };
  const moveIndicator = () => placeIndicator(active);
  links.forEach(a => { a.addEventListener('mouseenter', () => placeIndicator(a)); a.addEventListener('focus', () => placeIndicator(a)); });
  $('#navLinks')?.addEventListener('mouseleave', moveIndicator);

  const local = links.filter(a => a.getAttribute('href').startsWith('#'));
  if (local.length) {
    const sections = local.map(a => $(a.getAttribute('href')));
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (!e.isIntersecting) return;
      const i = sections.indexOf(e.target);
      local.forEach((l, j) => i === j ? l.setAttribute('aria-current', 'true') : l.removeAttribute('aria-current'));
      active = local[i]; moveIndicator();
    }), { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(s => s && io.observe(s));
    const clear = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { local.forEach(l => l.removeAttribute('aria-current')); active = null; moveIndicator(); }
    }), { rootMargin: '-45% 0px -50% 0px' });
    ['#top', '#pomoc'].forEach(s => $(s) && clear.observe($(s)));
  }
  requestAnimationFrame(moveIndicator);

  /* ---------- Mobile drawer ---------- */
  const burger = $('.burger'), drawer = $('#drawer');
  const setDrawer = open => {
    drawer.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Zamknij menu' : 'Otwórz menu');
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) $('a', drawer).focus({ preventScroll: true });
  };
  burger?.addEventListener('click', () => setDrawer(!drawer.classList.contains('is-open')));
  $$('a', drawer).forEach(a => a.addEventListener('click', () => setDrawer(false)));
  document.addEventListener('keydown', e => {
    if (!drawer?.classList.contains('is-open')) return;
    if (e.key === 'Escape') { setDrawer(false); burger.focus(); }
    if (e.key === 'Tab') {
      const f = [burger, ...$$('a', drawer)], i = f.indexOf(document.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
    }
  });

  /* ---------- Hero: gentle 3D tilt of the photo, note card drifts the other way ---------- */
  const media = $('#heroMedia');
  if (media && fine && !reduce) {
    const frame = $('.hero__frame', media), note = $('.note', media);
    media.addEventListener('pointermove', e => {
      const r = media.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      frame.style.setProperty('--ry', (x * 5).toFixed(2) + 'deg');
      frame.style.setProperty('--rx', (y * -4).toFixed(2) + 'deg');
      note.style.setProperty('--nx', (x * -14).toFixed(1) + 'px');
      note.style.setProperty('--ny', (y * -10).toFixed(1) + 'px');
    });
    media.addEventListener('pointerleave', () => {
      ['--ry', '--rx'].forEach(p => frame.style.setProperty(p, '0deg'));
      ['--nx', '--ny'].forEach(p => note.style.setProperty(p, '0px'));
    });
  }

  /* ---------- Tiles: cursor spotlight ---------- */
  if (fine) $$('.tile').forEach(t => t.addEventListener('pointermove', e => {
    const r = t.getBoundingClientRect();
    t.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    t.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }));

  /* ---------- Prefill topic from any [data-topic] link ---------- */
  const topic = $('#topic');
  const setTopic = name => {
    if (!topic || !name) return;
    const opt = [...topic.options].find(o => o.textContent.trim() === name);
    if (opt) topic.value = opt.value;
  };
  $$('[data-topic]').forEach(el => el.addEventListener('click', () => {
    setTopic(el.dataset.topic);
    setTimeout(() => $('#name')?.focus({ preventScroll: true }), 650);
  }));
  const q = new URLSearchParams(location.search).get('temat');
  if (q) setTopic(q);

  /* ---------- Areas: index list drives the framed photo (wipe) ---------- */
  const idx = $('#idx'), frame = $('#frame');
  if (idx && frame) {
    const items = $$('.idx__item', idx), imgs = $$('img', frame), cap = $('.frame__cap', frame);
    let cur = 0, timer = null;
    const upgrade = () => imgs.forEach(im => { if (im.dataset.full && innerWidth > 700) { im.src = im.dataset.full; delete im.dataset.full; } });
    const set = i => {
      if (i === cur) return;
      imgs.forEach((im, j) => { im.classList.toggle('was-active', j === cur); im.classList.toggle('is-active', j === i); });
      items.forEach((it, j) => it.classList.toggle('is-active', j === i));
      cap.innerHTML = $('.idx__icon', items[i]).innerHTML + `<span>${$('.idx__name', items[i]).textContent}</span>`;
      cur = i;
    };
    const stop = () => { clearInterval(timer); timer = null; };
    items.forEach((it, i) => {
      it.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') set(i); });
      it.addEventListener('focus', () => set(i));
    });
    new IntersectionObserver(([e]) => {
      if (e.isIntersecting) { upgrade(); if (touch && !reduce && !timer) timer = setInterval(() => set((cur + 1) % items.length), 3500); }
      else stop();
    }, { rootMargin: '300px 0px' }).observe(frame);
  }

  /* ---------- Buttons: fill blooms from where the cursor enters ---------- */
  if (fine) $$('.btn').forEach(b => b.addEventListener('pointerenter', e => {
    const r = b.getBoundingClientRect();
    b.style.setProperty('--bx', (e.clientX - r.left) + 'px');
    b.style.setProperty('--by', (e.clientY - r.top) + 'px');
  }));

  /* ---------- Process: steps switch the photo (wipe), auto-advance while visible ---------- */
  const ledger = $('#ledger');
  if (ledger) {
    const steps = $$('.step', ledger), photos = $$('#photos img');
    const DUR = 6000; let cur = 0, timer = null, visible = false, paused = false;
    ledger.style.setProperty('--dur', DUR + 'ms');
    const go = i => {
      if (i === cur) return;
      photos.forEach((p, j) => { p.classList.toggle('was-active', j === cur); p.classList.toggle('is-active', j === i); });
      steps.forEach((s, j) => {
        s.classList.toggle('is-active', j === i);
        $('button', s).setAttribute('aria-pressed', String(j === i));
        const bar = $('.step__bar', s); bar.style.animation = 'none'; void bar.offsetWidth; bar.style.animation = '';
      });
      cur = i; schedule();
    };
    const schedule = () => {
      clearTimeout(timer);
      if (reduce || !visible || paused) return;
      timer = setTimeout(() => go((cur + 1) % steps.length), DUR);
    };
    steps.forEach((s, i) => {
      const b = $('button', s);
      b.addEventListener('click', () => go(i));
      b.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') go(i); });
    });
    const pause = v => { paused = v; ledger.classList.toggle('is-paused', v); if (v) clearTimeout(timer); else schedule(); };
    ledger.addEventListener('pointerenter', () => pause(true));
    ledger.addEventListener('pointerleave', () => pause(false));
    ledger.addEventListener('focusin', () => pause(true));
    ledger.addEventListener('focusout', () => pause(false));
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; schedule(); }, { threshold: .35 }).observe(ledger);
    if (reduce) ledger.classList.add('is-paused');
  }

  /* ---------- Checklist meter (local only, not stored) ---------- */
  $$('.checklist').forEach(list => {
    const boxes = $$('input', list), wrap = list.parentElement, meter = $('.prep__meter', wrap);
    if (!meter) return;
    const upd = () => {
      const n = boxes.filter(b => b.checked).length;
      $('[data-count]', meter).textContent = n === boxes.length ? 'Wszystko gotowe. Możemy rozmawiać.' : `Gotowe: ${n} z ${boxes.length}`;
      $('b', meter).style.setProperty('--p', n / boxes.length);
    };
    boxes.forEach(b => b.addEventListener('change', upd));
  });

  /* ---------- Copy e-mail on long press / right click alternative: Alt+click copies ---------- */
  $$('[data-copy]').forEach(a => a.addEventListener('click', e => {
    if (!e.altKey || !navigator.clipboard) return;
    e.preventDefault();
    navigator.clipboard.writeText(a.dataset.copy).then(() => { const s = $('span', a); const t = s.textContent; s.textContent = 'Skopiowano adres'; setTimeout(() => s.textContent = t, 1600); });
  }));

  /* ---------- Mobile call bar ---------- */
  if (contact) new IntersectionObserver(([e]) => { nearContact = e.isIntersecting; onScroll(); }, { rootMargin: '0px 0px -20% 0px' }).observe(contact);
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', moveIndicator);

  /* ---------- Form: Web3Forms, mailto fallback until a key is set ---------- */
  const form = $('#form');
  if (form) form.addEventListener('submit', async e => {
    e.preventDefault();
    if (form.botcheck.checked) return;
    const name = $('#name'), consent = $('#consent'), status = $('#status'), btn = $('button[type=submit]', form);
    let ok = true;
    $('#name-err').textContent = ''; $('#consent-err').textContent = ''; $('#f-name').classList.remove('has-error');
    status.textContent = ''; status.classList.remove('is-ok');
    if (!name.value.trim()) { $('#name-err').textContent = 'Wpisz imię i nazwisko.'; $('#f-name').classList.add('has-error'); ok = false; }
    if (!consent.checked) { $('#consent-err').textContent = 'Zaznacz zgodę, żebyśmy mogli odpowiedzieć.'; ok = false; }
    if (!ok) { (name.value.trim() ? consent : name).focus(); return; }
    const subject = `Strona Polfinans: ${$('#topic').value || 'nowa wiadomość'}`;
    const body = `${name.value}\n${$('#reach').value}\n\n${$('#msg').value}`;
    const key = form.dataset.key;
    if (!key || key.startsWith('TODO')) {
      location.href = `mailto:${form.dataset.mail}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      status.textContent = 'Otworzyliśmy Twój program pocztowy z gotową wiadomością. Wyślij ją stamtąd.';
      return;
    }
    btn.setAttribute('aria-busy', 'true'); status.textContent = 'Wysyłamy…';
    try {
      const r = await fetch('https://api.web3forms.com/submit', {
        method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ access_key: key, subject, from_name: 'Strona Polfinans', name: name.value, kontakt: $('#reach').value, temat: $('#topic').value, message: $('#msg').value })
      });
      const j = await r.json();
      if (!j.success) throw new Error(j.message);
      form.reset(); status.classList.add('is-ok');
      status.textContent = 'Dziękujemy. Wiadomość dotarła, odezwiemy się wkrótce.';
    } catch {
      status.innerHTML = `Nie udało się wysłać. Zadzwoń: <a href="tel:+48509064464">509 064 464</a> albo napisz na <a href="mailto:${form.dataset.mail}">${form.dataset.mail}</a>.`;
    } finally { btn.removeAttribute('aria-busy'); }
  });

  onScroll();
})();
