/* =====================================================================
   reference-motion-style — EDU PRIMITIVES P35..P46 (GSAP, seek-safe, deterministic)
   Per-scene educational mode (physics / chemistry). Load AFTER motion-primitives.js: it extends window.RMS
   with RMS.edu. Like the archival primitives, every function only adds tweens to the ONE paused master
   timeline at an absolute time; nothing plays by itself, nothing uses Math.random or the clock.
   Shapes and timings come from the edu reference; COLOURS do not: grounds, type and lines use the archival
   template (paper, ink, red, yellow, teal set) so the whole video is one palette (owner, 13 Oct 2026).
   Numbers: measured on the edu reference at 23.976 fps and converted to 30 fps frames
   (edu-style.md §5 gives the evidence frame numbers). "observed" = read off 1 s contact sheets, not fitted.
   Diagrams are built in SVG at load time from plain data, so the same code serves a hand-written scene
   (edu-scene-template.html) and the builder's `edu` scene type (RMS.edu.scene).
   ===================================================================== */
(function () {
  const RMS = window.RMS;
  if (!RMS) throw new Error("edu-primitives.js needs motion-primitives.js loaded first");
  const F = RMS.F;
  const NS = "http://www.w3.org/2000/svg";

  // ---------- measured specification (frames @30 fps, GSAP ease names) ----------
  const SPEC = {
    particle:  { dur: 10, ease: "back.out(1.7)" },                 // P36 body pop (small sphere)
    disc:      { dur: 32, ease: "sine.out" },                      // P36 big disc grow: 26 f@24, sine.out rmse .05 (f1657-1683)
    shell:     { dur: 24, stagger: 8, ease: "power1.inOut" },      // P37 orbit line-draw (observed)
    orbit:     { period: 9.0 },                                    // P37 seconds per turn of the inner shell (observed), linear
    collapse:  { dur: 93, ease: "power2.in" },                     // P37 cloud -> atom: 74 f@24, power2/3.in (f1190-1264)
    field:     { dur: 126, ease: "power1.out" },                   // P38 a family of lines: 4.1-4.7 s (f2048-2160, f4540-4638)
    arrow:     { dur: 9, ease: "back.out(3)" },                    // P39 arrow birth: 7 f@24, overshoot 26-36 % (f3981-3988)
    align:     { dur: 28, stagger: 5, ease: "power2.inOut" },      // P39 arrows turning together: grid settles in 3.9-5 s (observed)
    morph:     { dur: 32, ease: "sine.inOut" },                    // P40 shape -> shape (same span as the disc grow)
    term:      { dur: 10, dy: 18, ease: "power2.out" },            // P41 equation term
    row:       { dur: 10, dy: 14, ease: "power2.out" },            // P42 list row: 1 f jump + 7 f settle @24 (f1559, f1593)
    type:      { cps: 21 },                                        // P43 title typed linear "on twos": 21 letters in 24 f@24
    label:     { dur: 8, ease: "power2.out" },                     // P42 label next to a body
    bond:      { dur: 12, ease: "power1.inOut" },                  // P44 molecule bond draw (extension, not in the reference)
    out:       { dur: 6 },                                         // exits: quick fade (hidden under the next cut when possible)
    drift:     0.0083,                                             // P46 camera: the style's own constant drift, 0.83 %/s linear (A2)
  };

  // ---------- palette = the archival template (rtl.css tokens; gradients need literal colours) ----------
  const COL = {
    paper: "#ececec", dark: "#1c1b1a", ink: "#2f2f2f", line: "#2b4f4b", lineDark: "#c3e6e7", ring: "#c3e6e7",
    red: "#d1615e", force: "#e84c4c", yellow: "#f3e24a", white: "#eae9e4",
  };
  const GROUNDS = { paper: "paper", dark: "dark", bloom: "bloom", cream: "paper", navy: "dark", glow: "bloom" };   // old names still work
  const TONE_CLASS = { warm: "warm", cool: "cool", key: "key", orange: "warm", purple: "cool", gold: "key", red: "key" };
  const TONES = {                       // body gradients, top -> bottom: warm = the style's red (a shade deeper so a white symbol passes 3:1), cool = its teal set
    proton:   ["#e58a86", "#c9524f", "#9c3a37"], plus: ["#e58a86", "#c9524f", "#9c3a37"],
    electron: ["#7fbfb9", "#339791", "#2b4f4b"], minus: ["#7fbfb9", "#339791", "#2b4f4b"],
    neutron:  ["#f4f3ee", "#cfcdc4", "#9a978d"],
    nucleus:  ["#5a5856", "#403e3d", "#262524"],
    red:      ["#e58a86", "#c9524f", "#9c3a37"], blue: ["#8fb4d9", "#3f78ae", "#27496d"],
    teal:     ["#7fbfb9", "#339791", "#2b4f4b"], light: ["#ffffff", "#f1f0ea", "#d6d4cb"], dark: ["#6a6866", "#403e3d", "#1c1b1a"],
    green:    ["#b9c98f", "#7d8f55", "#515734"], gold: ["#fdf3b0", "#f3e24a", "#dcb153"],
  };
  const WARM = /^(neutron|gold|light|green)$/;   // light bodies carry an ink symbol (white fails 3:1 on them)

  // ---------- tiny DOM helpers ----------
  const q = (s) => (typeof s === "string" ? document.querySelector(s) : s);
  function sv(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs || {}) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function el(tag, cls, parent, html) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    if (parent) parent.appendChild(e);
    return e;
  }
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const r2 = (n) => Math.round(n * 100) / 100;
  const piv = (...nodes) => nodes.forEach((n) => gsap.set(n, { svgOrigin: "0 0" }));   // pivot = the group's own origin

  // ======================= STAGE =======================
  // P35 EDU_GROUND: the style's halftone paper (or its charcoal) + the 72 px grid. Grounds change by a hard cut (two scenes).
  // root = an element inside the scene's .cam; hud = optional element inside the .hud (titles stay steady).
  function stage(root, o = {}) {
    const r = q(root);
    const comp = r.closest("[data-composition-id]");
    const W = +(o.W || (comp && comp.getAttribute("data-width")) || 1920), H = +(o.H || (comp && comp.getAttribute("data-height")) || 1080);
    const ground = GROUNDS[o.ground] || "paper", id = o.id || r.id || "edu", onDark = ground === "dark";
    r.classList.add("edu-root"); if (onDark) r.classList.add("on-dark");
    r.style.position = "absolute"; r.style.inset = "0";
    el("div", `edu-ground ${ground}`, r); if (o.grid !== false) el("div", "edu-grid", r);
    const svg = sv("svg", { class: "edu-svg", viewBox: `0 0 ${W} ${H}`, id: `${id}-svg` }, r);
    const defs = sv("defs", {}, svg);
    const dots = sv("pattern", { id: `${id}-dots`, width: 9, height: 9, patternUnits: "userSpaceOnUse", patternTransform: "rotate(30)" }, defs);
    sv("circle", { cx: 4.5, cy: 4.5, r: 1.7, fill: "#ffffff", "fill-opacity": 0.34 }, dots);
    const txt = el("div", "edu-txt", r);
    let hud = o.hud ? q(o.hud) : null;
    if (hud) { hud.classList.add("edu-txt"); if (onDark) hud.classList.add("on-dark"); }
    return { root: r, svg, defs, txt, hud: hud || txt, W, H, id, ground, onDark, items: {}, n: 0,
             px: (x) => (x / 100) * W, py: (y) => (y / 100) * H };
  }
  function grad(ctx, tone) {
    const key = Array.isArray(tone) ? tone.join("-").replace(/#/g, "") : tone;
    const gid = `${ctx.id}-g-${key}`;
    if (!ctx.defs.querySelector(`#${CSS.escape(gid)}`)) {
      const c = Array.isArray(tone) ? tone : TONES[tone] || TONES.light;
      const g = sv("linearGradient", { id: gid, x1: 0.2, y1: 0, x2: 0.8, y2: 1 }, ctx.defs);
      c.forEach((col, i) => sv("stop", { offset: i / (c.length - 1), "stop-color": col }, g));
    }
    return `url(#${gid})`;
  }
  function uid(ctx, o, kind) { return `${ctx.id}-${o.id || kind + ++ctx.n}`; }
  // text anchored on a point: the anchor carries left/top, GSAP owns the child's transform (no CSS transform to fight)
  function textAt(ctx, cls, html, x, y, o = {}) {
    const a = el("div", "edu-anchor", o.hud ? ctx.hud : ctx.txt); a.style.left = `${x}px`; a.style.top = `${y}px`;
    const t = el("div", `${cls}${o.ltr ? " ltr" : " ar"}`, a, html);
    if (o.id) t.id = o.id;
    gsap.set(t, { xPercent: o.align === "start" ? 0 : o.align === "end" ? -100 : -50, yPercent: -50 });
    return t;
  }

  // ======================= P36 BODIES =======================
  // A body = flat two-tone sphere with a halftone lower half and an optional symbol. Built centred on (0,0)
  // inside an outer <g> that carries the position, so pops / turns pivot on the centre (svgOrigin 0 0).
  function sphere(ctx, parent, d, tone, sym, o = {}) {
    const r = d / 2, g = sv("g", {}, parent);
    sv("circle", { r, fill: grad(ctx, tone) }, g);
    const cid = `${ctx.id}-c${++ctx.n}`;
    const cp = sv("clipPath", { id: cid }, ctx.defs); sv("circle", { r }, cp);
    const half = sv("g", { "clip-path": `url(#${cid})` }, g);
    sv("rect", { x: -r, y: r * 0.08, width: d, height: r, fill: `url(#${ctx.id}-dots)` }, half);
    if (sym) {
      const m = /^(.*?)([+\-−0⁰]?)$/.exec(sym), base = m[1] || sym, sign = m[1] ? m[2] : "";
      const t = sv("text", { x: sign ? -r * 0.1 : 0, y: r * 0.3, "text-anchor": "middle", "font-family": '"RMS Text", serif', "font-weight": 700,
                             "font-size": r2(d * (o.symScale || 0.56)), fill: o.symColor || (WARM.test(String(tone)) ? COL.ink : "#ffffff") }, g);
      t.textContent = base;
      if (sign) { const s = sv("tspan", { dy: -r * 0.42, "font-size": r2(d * 0.34) }, t); s.textContent = sign === "-" ? "−" : sign; }
    }
    return g;
  }
  function particle(ctx, o) {
    const id = uid(ctx, o, "p"), x = ctx.px(o.x), y = ctx.py(o.y), d = o.d || 114;
    const outer = sv("g", { id }, ctx.svg), inner = sv("g", { id: `${id}-in` }, outer);
    gsap.set(outer, { x, y }); piv(inner);
    if (o.ring) sv("ellipse", { rx: d * 0.74, ry: d * 0.2, fill: "none", stroke: COL.ring, "stroke-width": Math.max(5, d * 0.06) }, inner);
    sphere(ctx, inner, d, o.tone || "plus", o.sym, o);
    const it = { kind: "particle", id, outer, inner, x, y, d, q: o.q != null ? o.q : /minus|electron/.test(o.tone || "") ? -1 : 1 };
    ctx.items[o.id || id] = it; return it;
  }
  function pop(tl, it, at, big) {                      // small bodies overshoot a little; big discs swell without
    const s = big ? SPEC.disc : SPEC.particle;
    tl.fromTo(it.inner || it, { scale: 0, svgOrigin: "0 0" }, { scale: 1, duration: F(s.dur), ease: s.ease }, at);
    return F(s.dur);
  }

  // ======================= P37 ATOM =======================
  // cloud (the "we don't know yet" picture) collapses into nucleus + shells; electrons ride their shells.
  function atom(ctx, o) {
    const id = uid(ctx, o, "atom"), x = ctx.px(o.x), y = ctx.py(o.y);
    const outer = sv("g", { id }, ctx.svg); gsap.set(outer, { x, y });
    const line = ctx.onDark ? COL.lineDark : COL.line, nuc = o.nucleus || {};
    let cloud = null;
    if (o.cloud !== false) {
      const R = o.cloud_r || ((o.shells || [{ r: 200 }]).slice(-1)[0].r * 1.12);
      const gid = `${id}-cg`, rg = sv("radialGradient", { id: gid }, ctx.defs);
      [["0", "#339791", 0.9], ["0.45", "#7fbfb9", 0.6], ["1", "#c3e6e7", 0]].forEach(([of, c, a]) => sv("stop", { offset: of, "stop-color": c, "stop-opacity": a }, rg));
      cloud = sv("g", { id: `${id}-cloud` }, outer);
      sv("circle", { r: R, fill: `url(#${gid})` }, cloud);
      sv("circle", { r: R * 0.92, fill: `url(#${ctx.id}-dots)`, opacity: 0.9 }, cloud);
    }
    const shells = (o.shells || []).map((s, i) => {
      const c = sv("circle", { id: `${id}-sh${i}`, r: s.r, fill: "none", stroke: line, "stroke-width": 2.5, transform: "rotate(-90)" }, outer);
      const rotor = sv("g", { id: `${id}-rot${i}` }, outer), es = []; piv(rotor);
      for (let k = 0; k < (s.electrons || 0); k++) {
        const a = (k / s.electrons) * Math.PI * 2 + (s.phase || 0);
        const eg = sv("g", { transform: `translate(${r2(Math.cos(a) * s.r)},${r2(Math.sin(a) * s.r)})` }, rotor);
        const ein = sv("g", {}, eg); piv(ein); sphere(ctx, ein, s.ed || 38, "electron", s.sym === false ? "" : "e-"); es.push(ein);
      }
      return { c, rotor, es, r: s.r, period: s.period, dir: s.dir || (i % 2 ? -1 : 1) };
    });
    const nin = sv("g", { id: `${id}-nuc` }, outer); piv(nin); if (cloud) piv(cloud);
    if (nuc.balls) {                                    // protons / neutrons packed in the nucleus
      const nd = nuc.d || 96, n = nuc.balls.length, mid = n > 4, ring = mid ? n - 1 : n, bd = nd * (mid ? 0.42 : 0.52);
      nuc.balls.forEach((tone, k) => {
        const onRing = !(mid && k === n - 1);            // more than 4: the last one sits in the middle, on top
        const a = (k / ring) * Math.PI * 2 - Math.PI / 2, rr = onRing && n > 1 ? nd * (mid ? 0.3 : 0.24) : 0;
        const bg = sv("g", { transform: `translate(${r2(Math.cos(a) * rr)},${r2(Math.sin(a) * rr)})` }, nin);
        sphere(ctx, bg, bd, tone, tone === "proton" ? "p+" : tone === "neutron" ? "n" : "", { symScale: 0.5 });
      });
    } else sphere(ctx, nin, nuc.d || 96, nuc.tone || "nucleus", nuc.sym);
    const it = { kind: "atom", id, outer, inner: nin, cloud, shells, x, y, d: nuc.d || 96, q: 1 };
    ctx.items[o.id || id] = it; return it;
  }
  // at = the moment the cloud appears; reveal = when it collapses into the model (the word that names it)
  function atomBuild(tl, a, at, reveal, end) {
    const c = SPEC.collapse, s = SPEC.shell, hasCloud = !!a.cloud;
    let t = reveal != null ? reveal : at;
    if (hasCloud) {
      tl.fromTo(a.cloud, { opacity: 0, scale: 0.86, svgOrigin: "0 0" }, { opacity: 1, scale: 1, duration: F(10), ease: "power2.out" }, at);
      tl.to(a.cloud, { scale: 0.3, opacity: 0, duration: F(c.dur), ease: c.ease }, t);
      t += F(c.dur) * 0.55;                             // the model is born while the cloud is still closing
    }
    tl.fromTo(a.inner, { scale: 0, svgOrigin: "0 0" }, { scale: 1, duration: F(SPEC.disc.dur), ease: SPEC.disc.ease }, t);
    a.shells.forEach((sh, i) => {
      const L = 2 * Math.PI * sh.r, ts = t + F(6 + i * s.stagger);
      tl.fromTo(sh.c, { strokeDasharray: `${r2(L)} ${r2(L)}`, strokeDashoffset: r2(L) }, { strokeDashoffset: 0, duration: F(s.dur), ease: s.ease }, ts);
      sh.es.forEach((e, k) => tl.fromTo(e, { scale: 0, svgOrigin: "0 0" }, { scale: 1, duration: F(SPEC.particle.dur), ease: SPEC.particle.ease }, ts + F(s.dur - 6 + k * 3)));
      if (end != null) {                                // electrons never stop: linear turn for the rest of the scene
        const per = sh.period || SPEC.orbit.period * (1 + i * 0.55), dur = Math.max(0.1, end - ts);
        tl.fromTo(sh.rotor, { rotation: 0, svgOrigin: "0 0" }, { rotation: sh.dir * 360 * (dur / per), duration: dur, ease: "none" }, ts);
      }
    });
    return t;
  }

  // ======================= P38 FIELD LINES =======================
  // Real field lines of point sources (charges / magnetic poles): streamlines of E integrated from every
  // positive source (or backwards from negative ones when there is no positive). sources: [{x, y, q, r}] in px.
  function fieldPaths(sources, o = {}) {
    const n = o.n || 12, step = o.step || 7, maxSteps = o.maxSteps || 900, W = o.W || 1920, H = o.H || 1080, pad = o.pad || 260;
    const pos = sources.filter((s) => s.q > 0), starts = pos.length ? pos : sources, sign = pos.length ? 1 : -1, out = [];
    const E = (x, y) => {
      let ex = 0, ey = 0;
      for (const s of sources) { const dx = x - s.x, dy = y - s.y, d2 = dx * dx + dy * dy + 1e-6, d3 = d2 * Math.sqrt(d2); ex += (s.q * dx) / d3; ey += (s.q * dy) / d3; }
      const m = Math.hypot(ex, ey) || 1; return [(sign * ex) / m, (sign * ey) / m];
    };
    starts.forEach((s) => {
      const r0 = (s.r || 57) + 5, k = Math.max(4, Math.round(n * Math.abs(s.q)));
      for (let i = 0; i < k; i++) {
        const a = ((i + 0.5) / k) * Math.PI * 2 + (o.phase || 0);
        let x = s.x + Math.cos(a) * r0, y = s.y + Math.sin(a) * r0, pts = [[x, y]], hit = false;
        for (let j = 0; j < maxSteps; j++) {
          const [ex, ey] = E(x, y), [fx, fy] = E(x + (ex * step) / 2, y + (ey * step) / 2);   // midpoint (RK2)
          x += fx * step; y += fy * step;
          if (x < -pad || x > W + pad || y < -pad || y > H + pad) break;
          for (const t of sources) if (t !== s && Math.hypot(x - t.x, y - t.y) < (t.r || 57) + 4) { hit = true; break; }
          if (j % 2 === 1 || hit) pts.push([x, y]);
          if (hit) break;
        }
        if (pts.length > 3) out.push({ d: "M" + pts.map((p) => `${r2(p[0])} ${r2(p[1])}`).join("L"), closed: hit, len: pts.length });
      }
    });
    out.sort((a, b) => a.len - b.len);                  // short (inner) lines first: the field grows outwards
    return out;
  }
  function field(ctx, o) {
    const id = uid(ctx, o, "field"), g = sv("g", { id, fill: "none", "stroke-linecap": "round" }, null);
    ctx.svg.insertBefore(g, ctx.svg.children[1] || null);                // under the bodies
    const src = (o.sources || []).map((s) => {
      if (typeof s !== "string") return { x: ctx.px(s.x), y: ctx.py(s.y), q: s.q, r: s.r || 8 };
      const it = ctx.items[s]; return { x: it.x, y: it.y, q: it.q, r: it.d / 2 };
    });
    const col = o.color || (ctx.onDark ? COL.lineDark : COL.line);
    const paths = fieldPaths(src, { n: o.n, W: ctx.W, H: ctx.H, phase: o.phase }).map((p, i) =>
      sv("path", { id: `${id}-l${i}`, d: p.d, stroke: col, "stroke-width": o.w || 2, "stroke-opacity": o.opacity || 0.9 }, g));
    const it = { kind: "field", id, g, paths }; ctx.items[o.id || id] = it; return it;
  }
  function fieldDraw(tl, f, at, dur) {                  // every line draws from its source; inner lines lead
    const D = dur != null ? dur : F(SPEC.field.dur), n = f.paths.length || 1;
    f.paths.forEach((p, i) => {
      const L = p.getTotalLength(), st = at + (i / n) * D * 0.45, d = D * 0.55;
      tl.fromTo(p, { strokeDasharray: `${r2(L)} ${r2(L)}`, strokeDashoffset: r2(L) }, { strokeDashoffset: 0, duration: d, ease: SPEC.field.ease }, st);
    });
    return D;
  }

  // ======================= P39 ARROWS (force / spin / velocity) =======================
  // Born from the body: grows along its own axis from the tail with a clear overshoot (the only bounce in this mode).
  function arrow(ctx, o) {
    const id = uid(ctx, o, "arr");
    let x = o.x != null ? ctx.px(o.x) : 0, y = o.y != null ? ctx.py(o.y) : 0;
    const ang = o.angle || 0, len = o.len || 150, w = o.w || 9, head = o.head || w * 2.6;
    if (o.from) { const b = ctx.items[o.from], gap = b.d / 2 + (o.gap != null ? o.gap : 10), a = (ang * Math.PI) / 180; x = b.x + Math.cos(a) * gap; y = b.y + Math.sin(a) * gap; }
    const outer = sv("g", { id }, ctx.svg), turn = sv("g", { id: `${id}-turn` }, outer), inner = sv("g", { id: `${id}-in` }, turn);
    gsap.set(outer, { x, y }); piv(turn, inner); gsap.set(turn, { rotation: ang });
    const col = o.color || (ctx.onDark ? "#ffffff" : COL.ink);
    sv("line", { x1: 0, y1: 0, x2: len - head * 0.9, y2: 0, stroke: col, "stroke-width": w, "stroke-linecap": "round" }, inner);
    sv("path", { d: `M${len} 0L${len - head * 1.25} ${-head * 0.72}L${len - head * 1.25} ${head * 0.72}Z`, fill: col }, inner);
    const it = { kind: "arrow", id, outer, turn, inner, x, y, angle: ang, len }; ctx.items[o.id || id] = it; return it;
  }
  function arrowGrow(tl, a, at) {
    tl.fromTo(a.inner, { scaleX: 0, scaleY: 0.6, svgOrigin: "0 0" }, { scaleX: 1, scaleY: 1, duration: F(SPEC.arrow.dur), ease: SPEC.arrow.ease }, at);
    return F(SPEC.arrow.dur);
  }
  function arrowScale(tl, a, at, to, dur) {             // the force changes: same arrow, new length (never a new arrow)
    tl.to(a.inner, { scaleX: to, duration: dur != null ? dur : F(SPEC.align.dur), ease: SPEC.align.ease }, at);
  }
  function arrowsAlign(tl, arrows, at, angle) {         // many arrows turn to one direction, staggered
    arrows.forEach((a, i) => tl.to(a.turn, { rotation: angle, duration: F(SPEC.align.dur), ease: SPEC.align.ease }, at + F(SPEC.align.stagger * i)));
  }

  // bar magnet: red -> violet -> blue, pole letters; poles are field sources (N = +1 at the top end)
  function magnet(ctx, o) {
    const id = uid(ctx, o, "mag"), x = ctx.px(o.x), y = ctx.py(o.y), w = o.w || 200, h = o.h || 520;
    const outer = sv("g", { id }, ctx.svg), inner = sv("g", { id: `${id}-in` }, outer); gsap.set(outer, { x, y }); piv(inner);
    const gid = `${id}-g`, lg = sv("linearGradient", { id: gid, x1: 0, y1: 0, x2: 0, y2: 1 }, ctx.defs);
    [["0", "#d1615e"], ["0.3", "#d1615e"], ["0.5", "#8a5f86"], ["0.72", "#3f78ae"], ["1", "#3f78ae"]].forEach(([of, c]) => sv("stop", { offset: of, "stop-color": c }, lg));
    sv("rect", { x: -w / 2, y: -h / 2, width: w, height: h, fill: `url(#${gid})` }, inner);
    sv("rect", { x: -w / 2, y: -h / 2, width: w, height: h, fill: `url(#${ctx.id}-dots)`, opacity: 0.55 }, inner);
    (o.poles || ["N", "S"]).forEach((p, i) => {
      const t = sv("text", { x: 0, y: (i ? 1 : -1) * (h / 2 - w * 0.42) + w * 0.26, "text-anchor": "middle", "font-family": '"RMS Text", serif', "font-weight": 700, "font-size": r2(w * 0.74), fill: "#ffffff" }, inner);
      t.textContent = p;
    });
    const it = { kind: "magnet", id, outer, inner, x, y, d: w, w, h,
                 poles: [{ x, y: y - h / 2 + w * 0.3, q: 1, r: w * 0.34 }, { x, y: y + h / 2 - w * 0.3, q: -1, r: w * 0.34 }] };
    ctx.items[o.id || id] = it; return it;
  }

  // ======================= P40 MORPH =======================
  // Shape -> shape without a plugin: both outlines are sampled at the same N points, so GSAP can tween `d`.
  // kind: circle {cx,cy,r} | rect {cx,cy,w,h,rx} | blob {cx,cy,r,seed,amp}
  function shapePath(kind, o, N = 72) {
    const pts = [];
    if (kind === "rect") {
      const { cx, cy, w, h } = o, rx = Math.min(o.rx || 0, w / 2, h / 2), P = 2 * (w + h - 4 * rx) + 2 * Math.PI * rx;
      for (let i = 0; i < N; i++) {
        let d = (i / N) * P + w / 2 - rx, x, y;            // start at top centre, clockwise
        const segs = [w - 2 * rx, (Math.PI * rx) / 2, h - 2 * rx, (Math.PI * rx) / 2, w - 2 * rx, (Math.PI * rx) / 2, h - 2 * rx, (Math.PI * rx) / 2];
        let k = 0; d = d % P; while (d > segs[k]) { d -= segs[k]; k = (k + 1) % 8; }
        const L = cx - w / 2, R = cx + w / 2, T = cy - h / 2, B = cy + h / 2, a = rx ? d / rx : 0;
        if (k === 0) { x = L + rx + d; y = T; } else if (k === 1) { x = R - rx + Math.sin(a) * rx; y = T + rx - Math.cos(a) * rx; }
        else if (k === 2) { x = R; y = T + rx + d; } else if (k === 3) { x = R - rx + Math.cos(a) * rx; y = B - rx + Math.sin(a) * rx; }
        else if (k === 4) { x = R - rx - d; y = B; } else if (k === 5) { x = L + rx - Math.sin(a) * rx; y = B - rx + Math.cos(a) * rx; }
        else if (k === 6) { x = L; y = B - rx - d; } else { x = L + rx - Math.cos(a) * rx; y = T + rx - Math.sin(a) * rx; }
        pts.push([x, y]);
      }
    } else {
      const rnd = RMS.rng(o.seed || "blob"), amp = kind === "blob" ? o.amp || 0.16 : 0;
      const w1 = rnd() * 6.28, w2 = rnd() * 6.28, w3 = rnd() * 6.28;
      for (let i = 0; i < N; i++) {
        const a = (i / N) * Math.PI * 2 - Math.PI / 2;
        const k = 1 + amp * (0.5 * Math.sin(2 * a + w1) + 0.32 * Math.sin(3 * a + w2) + 0.18 * Math.sin(5 * a + w3));
        pts.push([o.cx + Math.cos(a) * o.r * k, o.cy + Math.sin(a) * o.r * k]);
      }
    }
    return "M" + pts.map((p) => `${r2(p[0])} ${r2(p[1])}`).join("L") + "Z";
  }
  function morph(tl, path, toD, at, dur, ease) {
    tl.to(q(path), { attr: { d: toD }, duration: dur != null ? dur : F(SPEC.morph.dur), ease: ease || SPEC.morph.ease }, at);
  }

  // ======================= P41 EQUATION BUILD-UP =======================
  // Always LTR. Mini markup inside a term: x^2  x_1  x^{-2}  (digits / signs only; Greek needs a Latin-math font).
  function mathHTML(s) {
    return esc(s).replace(/\^\{([^}]*)\}|\^(\S)/g, (m, a, b) => `<sup>${a || b}</sup>`).replace(/_\{([^}]*)\}|_(\S)/g, (m, a, b) => `<sub>${a || b}</sub>`).replace(/-/g, "−");
  }
  function equation(ctx, o) {
    const id = uid(ctx, o, "eq"), a = el("div", "edu-anchor", ctx.txt); a.style.left = `${ctx.px(o.x)}px`; a.style.top = `${ctx.py(o.y)}px`;
    const eq = el("div", "edu-eq", a); eq.id = id; if (o.size) eq.style.fontSize = `${o.size}px`;
    gsap.set(eq, { xPercent: -50, yPercent: -50 });
    const box = el("span", "box", eq); box.id = `${id}-box`;
    const terms = (o.terms || []).map((t, i) => {
      const sp = el("span", "term", eq); sp.id = `${id}-t${i}`;
      if (t.frac) {
        sp.classList.add("frac");
        const num = el("span", "num", sp, mathHTML(t.frac[0])), bar = el("span", "bar", sp), den = el("span", "den", sp, mathHTML(t.frac[1]));
        num.id = `${id}-t${i}n`; den.id = `${id}-t${i}d`;
        return { el: sp, num, bar, den, t: t.t, tone: t.tone };
      }
      sp.innerHTML = mathHTML(t.s);
      if (t.color) sp.style.color = t.color;
      return { el: sp, t: t.t, tone: t.tone };
    });
    const it = { kind: "equation", id, eq, terms, box }; ctx.items[o.id || id] = it; return it;
  }
  function eqBuild(tl, e, times) {                      // one term per spoken symbol; a fraction = bar, then top, then bottom
    const s = SPEC.term;
    gsap.set(e.box, { opacity: 0 });
    e.terms.forEach((t, i) => {
      const at = (times && times[i] != null ? times[i] : t.t) || 0;
      if (t.bar) {
        gsap.set(t.el, { opacity: 1 });
        tl.fromTo(t.bar, { scaleX: 0 }, { scaleX: 1, duration: F(8), ease: "power2.out" }, at);
        tl.fromTo(t.num, { opacity: 0, y: s.dy }, { opacity: 1, y: 0, duration: F(s.dur), ease: s.ease }, at + F(3));
        tl.fromTo(t.den, { opacity: 0, y: -s.dy }, { opacity: 1, y: 0, duration: F(s.dur), ease: s.ease }, at + F(9));
      } else tl.fromTo(t.el, { opacity: 0, y: s.dy }, { opacity: 1, y: 0, duration: F(s.dur), ease: s.ease }, at);
    });
  }
  function eqHighlight(tl, node, at, color, ctx) {      // the term the sentence is about: colour + underline drawn
    const ul = el("span", "ul", node); if (color) ul.style.background = color;
    tl.fromTo(ul, { scaleX: 0 }, { scaleX: 1, duration: F(RMS.SPEC.draw.dur), ease: RMS.SPEC.draw.ease }, at);
    tl.to(node, { color: color || (ctx && ctx.onDark ? COL.yellow : "#b94a47"), duration: F(8), ease: "none" }, at);
  }
  function eqBox(tl, e, at) {                           // the result: frame closes around the whole law
    tl.fromTo(e.box, { opacity: 0, scale: 1.08 }, { opacity: 1, scale: 1, duration: F(10), ease: "power2.out" }, at);
  }

  // ======================= P42 LABELS / LIST =======================
  function label(ctx, o) {
    const cls = `edu-label ${TONE_CLASS[o.tone] || ""}${o.small ? " small" : ""}`;
    let x = o.x != null ? ctx.px(o.x) : 0, y = o.y != null ? ctx.py(o.y) : 0;
    if (o.of) { const b = ctx.items[o.of]; x = b.x + (o.dx || 0); y = b.y + (o.dy != null ? o.dy : -(b.d / 2 + 54)); }
    const t = textAt(ctx, o.cls || cls, o.html || esc(o.text), x, y, { id: uid(ctx, o, "lb"), align: o.align, ltr: o.ltr, hud: o.hud });
    const it = { kind: "label", id: t.id, el: t, x, y }; ctx.items[o.id || t.id] = it; return it;
  }
  function labelIn(tl, l, at) {
    tl.fromTo(l.el, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: F(SPEC.label.dur), ease: SPEC.label.ease }, at);
  }
  const ICONS = {
    bolt: '<path d="M26 3 9 25h11l-4 16 19-24H23z" fill="currentColor"/>',
    mass: '<path d="M16 9h12v6H16z" fill="currentColor"/><path d="M9 15h26l4 24H5z" fill="currentColor"/>',
    magnet: '<path d="M9 40V20a13 13 0 0 1 26 0v20h-9V20a4 4 0 0 0-8 0v20z" fill="currentColor"/>',
    spin: '<path d="M22 6a16 16 0 1 0 16 16" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/><path d="M38 10v13H25z" fill="currentColor"/>',
    heat: '<path d="M22 3c6 9 12 13 12 22a12 12 0 0 1-24 0c0-5 3-8 5-12 2 4 4 5 5 5 1-5 1-9 2-15z" fill="currentColor"/>',
    drop: '<path d="M22 3c7 10 13 16 13 24a13 13 0 0 1-26 0c0-8 6-14 13-24z" fill="currentColor"/>',
    wave: '<path d="M3 22c5-14 9-14 14 0s9 14 14 0 7-12 10-6" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>',
    dot: '<circle cx="22" cy="22" r="9" fill="currentColor"/>',
  };
  function list(ctx, o) {
    const id = uid(ctx, o, "list"), a = el("div", "edu-anchor", ctx.txt); a.style.left = `${ctx.px(o.x)}px`; a.style.top = `${ctx.py(o.y)}px`;
    const box = el("div", "edu-list", a); box.id = id; gsap.set(box, { xPercent: -50 });
    const rows = (o.rows || []).map((r, i) => {
      const row = el("div", "edu-row ar", box, `<svg viewBox="0 0 44 44">${ICONS[r.icon] || ICONS.dot}</svg><span>${esc(r.text)}</span>`);
      row.id = `${id}-r${i}`; return { el: row, t: r.t };
    });
    const it = { kind: "list", id, rows }; ctx.items[o.id || id] = it; return it;
  }
  function rowsIn(tl, l, times) {                       // each row on the word that names it (never a fixed stagger)
    const s = SPEC.row;
    l.rows.forEach((r, i) => tl.fromTo(r.el, { opacity: 0, y: s.dy }, { opacity: 1, y: 0, duration: F(s.dur), ease: s.ease }, (times && times[i] != null ? times[i] : r.t) || 0));
  }

  // ======================= P43 TITLE =======================
  // Typed, linear, "on twos". Arabic letters must stay joined, so the line is never split per letter:
  // a stepped clip opens it from the reading start (right for Arabic), 2 letters per step, 21 letters / s.
  function title(ctx, o) {
    const id = uid(ctx, o, "title"), box = el("div", `edu-title${o.ltr ? " ltr" : " ar"}`, ctx.hud);
    box.id = id; const t = el("span", "t", box, esc(o.text)); t.id = `${id}-t`;
    let sub = null;
    if (o.sub) { sub = el("div", `edu-sub${o.ltr ? " ltr" : " ar"}`, ctx.hud, esc(o.sub)); sub.id = `${id}-sub`; }
    const it = { kind: "title", id, el: t, sub, chars: [...o.text].length, ltr: !!o.ltr }; ctx.items[o.id || id] = it; return it;
  }
  function titleType(tl, t, at, subAt) {
    const dur = Math.max(F(8), t.chars / SPEC.type.cps), steps = Math.max(3, Math.round(t.chars / 2));
    const from = t.ltr ? "inset(-25% 100% -25% -2%)" : "inset(-25% -2% -25% 100%)", to = "inset(-25% -2% -25% -2%)";
    tl.fromTo(t.el, { clipPath: from }, { clipPath: to, duration: dur, ease: `steps(${steps})` }, at);
    if (t.sub) tl.fromTo(t.sub, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: F(SPEC.label.dur), ease: SPEC.label.ease }, subAt != null ? subAt : at + dur + F(4));
    return dur;
  }

  // ======================= P44 MOLECULE (extension: same bodies, bonds drawn as lines) =======================
  // atoms: [{el:"O", x, y (px offsets from the centre), d, tone}], bonds: [[i, j, order]]
  function molecule(ctx, o) {
    const id = uid(ctx, o, "mol"), x = ctx.px(o.x), y = ctx.py(o.y);
    const outer = sv("g", { id }, ctx.svg), inner = sv("g", { id: `${id}-in` }, outer); gsap.set(outer, { x, y });
    const col = ctx.onDark ? "#ffffff" : COL.ink;
    const bonds = (o.bonds || []).map(([i, j, order = 1]) => {
      const a = o.atoms[i], b = o.atoms[j], dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy), nx = -dy / L, ny = dx / L, g = [];
      for (let k = 0; k < order; k++) {
        const off = (k - (order - 1) / 2) * 14;
        g.push(sv("line", { x1: r2(a.x + nx * off), y1: r2(a.y + ny * off), x2: r2(b.x + nx * off), y2: r2(b.y + ny * off), stroke: col, "stroke-width": 7, "stroke-linecap": "round" }, inner));
      }
      return { lines: g, L };
    });
    const atoms = (o.atoms || []).map((a) => {
      const g = sv("g", { transform: `translate(${a.x},${a.y})` }, inner), ain = sv("g", {}, g); piv(ain);
      sphere(ctx, ain, a.d || 110, a.tone || "light", a.el, { symColor: a.symColor, symScale: 0.5 });
      return ain;
    });
    const it = { kind: "molecule", id, outer, inner, atoms, bonds, x, y, d: o.d || 240, q: 0 }; ctx.items[o.id || id] = it; return it;
  }
  function moleculeBuild(tl, m, at, atomTimes) {        // atoms pop on their names, bonds are drawn once both ends exist
    m.atoms.forEach((a, i) => tl.fromTo(a, { scale: 0, svgOrigin: "0 0" }, { scale: 1, duration: F(SPEC.particle.dur), ease: SPEC.particle.ease }, atomTimes && atomTimes[i] != null ? atomTimes[i] : at + F(4 * i)));
    const last = atomTimes ? Math.max(...atomTimes) : at + F(4 * (m.atoms.length - 1));
    m.bonds.forEach((b, i) => b.lines.forEach((ln) => tl.fromTo(ln, { strokeDasharray: `${r2(b.L)} ${r2(b.L)}`, strokeDashoffset: r2(b.L) },
      { strokeDashoffset: 0, duration: F(SPEC.bond.dur), ease: SPEC.bond.ease }, last + F(6 + 4 * i))));
  }

  // ======================= P45 MOVES / EXITS, P46 CAMERA =======================
  function moveTo(tl, it, at, xPct, yPct, dur, ease, ctx) {
    const x = ctx.px(xPct), y = ctx.py(yPct);
    tl.to(it.outer, { x, y, duration: dur != null ? dur : F(SPEC.align.dur), ease: ease || SPEC.align.ease }, at);
    it.x = x; it.y = y;
  }
  function out(tl, it, at) {
    const node = it.outer || it.el || it.eq || it.g || it;
    tl.to(node, { opacity: 0, duration: F(SPEC.out.dur), ease: "none" }, at);
  }
  function drift(tl, cam, at, dur, o = {}) {            // P46 = P14: the style's constant linear drift on the whole diagram
    const s0 = o.s0 != null ? o.s0 : 1, s1 = o.s1 != null ? o.s1 : s0 + Math.min(0.2, SPEC.drift * dur);
    RMS.drift(tl, cam, at, dur, Object.assign({}, o, { s0, s1 }));
  }

  // ======================= declarative scene (used by the builder's `edu` type) =======================
  // spec: {ground, start, end, camera, items: [{kind, id, t, ...}]} — times are absolute VO seconds.
  function scene(tl, sid, spec) {
    const root = q(`#${sid}-edu`), hud = q(`#${sid}-eduhud`);
    const ctx = stage(root, { ground: spec.ground, id: sid, hud });
    const end = spec.end, made = [];
    (spec.items || []).forEach((o) => {
      const t = o.t != null ? o.t : spec.start;
      switch (o.kind) {
        case "title": { const it = title(ctx, o); titleType(tl, it, t, o.sub_t); break; }
        case "label": case "year": case "pill": case "note": {
          const cls = o.kind === "label" ? null : o.kind === "year" ? "year-badge" : o.kind === "pill" ? (o.tone === "black" ? "pill-black" : "pill-red") : "edu-note";
          const html = o.kind === "note" ? esc(o.text).replace(/\*(.+?)\*/g, '<span class="hl">$1</span>') : null;
          const it = label(ctx, Object.assign({}, o, { cls, html, ltr: o.ltr || o.kind === "year" })); labelIn(tl, it, t);
          if (o.out != null) out(tl, it, o.out); break;
        }
        case "particle": { const it = particle(ctx, o); pop(tl, it, t, (o.d || 114) > 300);
          if (o.label) { const l = label(ctx, Object.assign({ of: o.id }, o.label)); labelIn(tl, l, o.label.t != null ? o.label.t : t + F(6)); } break; }
        case "atom": { const it = atom(ctx, o); atomBuild(tl, it, t, o.reveal, end); break; }
        case "magnet": { const it = magnet(ctx, o); pop(tl, it, t, true); break; }
        case "field": {
          const srcs = (o.sources || []).flatMap((s) => (typeof s === "string" && ctx.items[s] && ctx.items[s].poles ? ctx.items[s].poles.map((p) => ({ x: (p.x / ctx.W) * 100, y: (p.y / ctx.H) * 100, q: p.q, r: p.r })) : [s]));
          const it = field(ctx, Object.assign({}, o, { sources: srcs })); fieldDraw(tl, it, t, o.dur);
          if (o.out != null) out(tl, it, o.out); break;
        }
        case "arrow": { const it = arrow(ctx, o); arrowGrow(tl, it, t);
          if (o.label) { const a = (it.angle * Math.PI) / 180, l = label(ctx, Object.assign({ x: ((it.x + Math.cos(a) * it.len * 0.5) / ctx.W) * 100, y: ((it.y + Math.sin(a) * it.len * 0.5 - 52) / ctx.H) * 100, small: true }, o.label)); labelIn(tl, l, t + F(5)); }
          if (o.out != null) out(tl, it, o.out); break; }
        case "molecule": { const it = molecule(ctx, o); moleculeBuild(tl, it, t, o.atom_times); break; }
        case "equation": { const it = equation(ctx, o); eqBuild(tl, it);
          (o.highlight || []).forEach((h) => eqHighlight(tl, h.part ? it.terms[h.term][h.part] : it.terms[h.term].el, h.t, h.color, ctx));
          if (o.box != null) eqBox(tl, it, o.box); break; }
        case "list": { const it = list(ctx, o); rowsIn(tl, it); break; }
        case "move": made.push(() => moveTo(tl, ctx.items[o.target], t, o.to[0], o.to[1], o.dur, o.ease, ctx)); break;
        case "scale": made.push(() => arrowScale(tl, ctx.items[o.target], t, o.to, o.dur)); break;
        case "align": made.push(() => arrowsAlign(tl, o.targets.map((k) => ctx.items[k]), t, o.angle)); break;
        case "out": made.push(() => out(tl, ctx.items[o.target], t)); break;
      }
    });
    made.forEach((fn) => fn());
    return ctx;
  }

  RMS.edu = {
    SPEC, COL, TONES, ICONS, stage, particle, pop, atom, atomBuild, fieldPaths, field, fieldDraw, arrow, arrowGrow, arrowScale,
    arrowsAlign, magnet, shapePath, morph, mathHTML, equation, eqBuild, eqHighlight, eqBox, label, labelIn, list, rowsIn,
    title, titleType, molecule, moleculeBuild, moveTo, out, drift, scene, sv,
  };
})();
