(() => {
  const header = document.querySelector(".masthead");
  const menu = document.querySelector(".mobile-menu");
  function scrollState() {
    header?.classList.toggle("raised", window.scrollY > 4);
  }
  window.addEventListener("scroll", scrollState, { passive: true });
  scrollState();
  document.addEventListener("keydown", event => {
    if (menu?.open && event.key === "Escape") {
      menu.open = false;
      menu.querySelector("summary").focus();
    }
  });
  document.addEventListener("click", event => {
    if (menu?.open && !menu.contains(event.target)) menu.open = false;
  });
  window.matchMedia("(min-width: 941px)").addEventListener("change", () => {
    if (menu) menu.open = false;
  });

  // These are unsaved enquiry lines. Renumber submitted field names, labels and
  // IDs together so Django always receives one contiguous formset.
  const form = document.querySelector(".quote-form");
  if (form) {
    const rows = form.querySelector("[data-quote-items]");
    const total = form.elements["items-TOTAL_FORMS"];
    const add = form.querySelector("[data-add-item]");
    const template = form.querySelector("[data-line-template]");
    function syncLines() {
      const lines = [...rows.querySelectorAll("[data-line]")];
      lines.forEach((line, index) => {
        for (const element of line.querySelectorAll("[name], [id], [for], [aria-describedby]")) {
          for (const attr of ["name", "id", "for", "aria-describedby"]) {
            if (element.hasAttribute(attr)) {
              element.setAttribute(attr, element.getAttribute(attr).replace(/items-\d+-/g, "items-" + index + "-"));
            }
          }
        }
        line.querySelector("[data-number]").textContent = index + 1;
        line.querySelector("[data-remove-item]").hidden = lines.length === 1;
      });
      total.value = lines.length;
      add.hidden = lines.length >= Number(form.elements["items-MAX_NUM_FORMS"].value);
    }
    add.addEventListener("click", () => {
      const index = Number(total.value);
      if (index >= Number(form.elements["items-MAX_NUM_FORMS"].value)) return;
      const next = document.createElement("template");
      next.innerHTML = template.innerHTML.replaceAll("__prefix__", index).replaceAll("__index__", index + 1);
      rows.append(next.content);
      syncLines();
      rows.lastElementChild.querySelector("select")?.focus();
    });
    rows.addEventListener("click", event => {
      const remove = event.target.closest("[data-remove-item]");
      if (!remove) return;
      remove.closest("[data-line]").remove();
      syncLines();
      add.focus();
    });
    syncLines();
  }

  const { gsap, ScrollTrigger } = window;
  if (!gsap || !ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  let media;
  function animate() {
    media = gsap.matchMedia();
    media.add("(prefers-reduced-motion: no-preference)", () => {
      const intro = document.querySelector(".hero-copy");
      if (intro) gsap.from(intro.children, { y: 12, opacity: 0, stagger: .07, duration: .48, clearProps: "all" });
      const shot = document.querySelector(".shot-mask");
      if (shot) gsap.from(shot, {clipPath: "inset(0 0 6% 0)", duration: .7, ease: "power2.out", clearProps: "clipPath"});
      for (const group of document.querySelectorAll("[data-stagger]")) {
        ScrollTrigger.batch(group.children, {
          start: "top 98%", once: true,
          onEnter: batch => gsap.from(batch, {y: 12, opacity: .72, duration: .4, stagger: .045, clearProps: "all"})
        });
      }
      for (const section of document.querySelectorAll(".editorial, .feature-grid")) {
        gsap.from(section, {y: 12, duration: .5, clearProps: "transform", scrollTrigger: {trigger: section, start: "top 95%", once: true}});
      }
      const featureImage = document.querySelector(".feature-photo img");
      if (featureImage && window.matchMedia("(min-width: 941px)").matches) {
        gsap.fromTo(featureImage, {scale: 1.06, yPercent: -2}, {yPercent: 2, ease: "none",
          scrollTrigger: {trigger: featureImage.parentElement, start: "top bottom", end: "bottom top", scrub: true}});
      }
    });
    ScrollTrigger.refresh();
  }
  animate();
  window.addEventListener("load", () => ScrollTrigger.refresh(), {once: true});
  document.fonts?.ready.then(() => ScrollTrigger.refresh());
  window.addEventListener("pagehide", () => media.revert());
  window.addEventListener("pageshow", event => { if (event.persisted) animate(); });
})();
