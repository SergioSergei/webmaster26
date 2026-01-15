/* =========================
   HIGHLIGHT CAROUSEL
   (SLIDE VIA CLASSES)
========================= */

const slides = document.querySelectorAll("[data-highlight-slide]");
const prevBtn = document.querySelector("[data-highlight-prev]");
const nextBtn = document.querySelector("[data-highlight-next]");

let currentIndex = 0;

function updateSlides(nextIndex, direction) {
  slides.forEach((slide, i) => {
    slide.classList.remove("is-active", "slide-left", "slide-right");

    if (i === nextIndex) {
      slide.classList.add("is-active");
      slide.classList.add(direction === "next" ? "slide-in-right" : "slide-in-left");
    }

    if (i === currentIndex) {
      slide.classList.add(direction === "next" ? "slide-out-left" : "slide-out-right");
    }
  });

  currentIndex = nextIndex;
}

function nextSlide() {
  const next = (currentIndex + 1) % slides.length;
  updateSlides(next, "next");
}

function prevSlide() {
  const prev = (currentIndex - 1 + slides.length) % slides.length;
  updateSlides(prev, "prev");
}

nextBtn?.addEventListener("click", nextSlide);
prevBtn?.addEventListener("click", prevSlide);

setInterval(nextSlide, 8000);

/* =========================
   CARD HOVER (CLASS ONLY)
========================= */

document.querySelectorAll(".card").forEach(card => {
  card.addEventListener("mouseenter", () => {
    card.classList.add("card-hover");
  });

  card.addEventListener("mouseleave", () => {
    card.classList.remove("card-hover");
  });
});

/* =========================
   PILL BUTTON MICRO-MOTION
========================= */

document.querySelectorAll(".pillBtn").forEach(btn => {
  btn.addEventListener("mouseenter", () => {
    btn.classList.add("pill-hover");
  });

  btn.addEventListener("mouseleave", () => {
    btn.classList.remove("pill-hover");
  });
});

/* =========================
   DIVERSITY FADE-IN
========================= */

const observer = new IntersectionObserver(
  entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("fade-in");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.25 }
);

document
  .querySelectorAll(".diversity__stats, .diversity__art, .diversity__badge")
  .forEach(el => observer.observe(el));