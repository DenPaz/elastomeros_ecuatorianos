// Hide the navbar when clicking outside of it or pressing Escape
(function () {
  const navbar = document.getElementById("navbarNav");
  const toggler = document.querySelector(".navbar-toggler");
  if (!navbar || !toggler) return;

  function hideNavbar() {
    if (!navbar.classList.contains("show")) return;
    bootstrap.Collapse.getOrCreateInstance(navbar).hide();
  }

  document.addEventListener("pointerdown", (event) => {
    if (!navbar.contains(event.target) && !toggler.contains(event.target)) {
      hideNavbar();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") hideNavbar();
  });
})();

// Page loading animation
(function () {
  window.addEventListener("load", function () {
    const preloader = document.querySelector(".page-loading");
    if (!preloader) return;

    preloader.classList.remove("active");

    setTimeout(function () {
      preloader.remove();
    }, 1500);
  });
})();

// Toast messages — server-rendered + HTMX HX-Trigger
(function () {
  function escapeHtml(text) {
    var div = document.createElement("div");
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  function resetBarAnimation(bar) {
    if (!bar) return;
    bar.style.animation = "none";
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        bar.style.animation = "";
        bar.style.animationPlayState = "running";
      });
    });
  }

  function initToast(el) {
    const DEFAULT_DELAY = 2000;
    const delay = parseInt(
      el.getAttribute("data-bs-delay") || DEFAULT_DELAY,
      10,
    );
    const bar = el.querySelector(".timer-bar");
    const controller = new AbortController();
    const signal = controller.signal;
    let timeoutId = null;

    el.style.setProperty("--toast-delay", delay + "ms");

    function start(ms) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(function () {
        bootstrap.Toast.getOrCreateInstance(el).hide();
      }, ms);
      if (bar) bar.style.animationPlayState = "running";
    }

    function pause() {
      clearTimeout(timeoutId);
      if (bar) bar.style.animationPlayState = "paused";
    }

    el.addEventListener(
      "shown.bs.toast",
      function () {
        resetBarAnimation(bar);
        start(delay);
      },
      { signal },
    );

    el.addEventListener(
      "hidden.bs.toast",
      function () {
        clearTimeout(timeoutId);
        controller.abort();
        el.remove();
      },
      { signal },
    );

    el.addEventListener(
      "mouseenter",
      function () {
        pause();
      },
      { signal },
    );

    el.addEventListener(
      "mouseleave",
      function () {
        resetBarAnimation(bar);
        start(delay);
      },
      { signal },
    );

    new bootstrap.Toast(el).show();
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("#toast-container .toast").forEach(initToast);
  });

  document.body.addEventListener("messages", function (event) {
    const container = document.getElementById("toast-container");
    if (!container) return;
    const messages = event.detail.value || event.detail;

    messages.forEach(function (msg) {
      const level = msg.tags || "info";
      const el = document.createElement("div");
      el.className = "toast fade text-bg-" + level;
      el.setAttribute("role", "alert");
      el.setAttribute("aria-live", "assertive");
      el.setAttribute("aria-atomic", "true");
      el.setAttribute("data-bs-autohide", "false");
      el.setAttribute("data-bs-delay", String(DEFAULT_DELAY));
      el.innerHTML =
        '<div class="d-flex justify-content-between align-items-center">' +
        '<div class="toast-body">' +
        escapeHtml(msg.message) +
        "</div>" +
        '<button type="button" class="btn-close btn-close-white me-3" ' +
        'data-bs-dismiss="toast" aria-label="Close"></button>' +
        "</div>" +
        '<div class="toast-timer"><div class="timer-bar"></div></div>';
      container.appendChild(el);
      initToast(el);
    });
  });
})();

// Initialize Swiper carousels on page load and after HTMX swaps or modals
(function () {
  if (typeof Swiper === "undefined") return;

  function initSwiper(root = document) {
    if (!(root instanceof Element || root instanceof Document)) return;
    root.querySelectorAll(".swiper-nav-onhover").forEach((el) => {
      if (el.swiper) {
        el.swiper.destroy();
      }
      const options = JSON.parse(el.dataset.swiperOptions || "{}");
      if (options.navigation) {
        options.navigation.prevEl = el.querySelector(".btn-prev");
        options.navigation.nextEl = el.querySelector(".btn-next");
      }
      new Swiper(el, options);
    });
  }

  document.addEventListener("DOMContentLoaded", () => initSwiper());
  document.addEventListener("htmx:afterSwap", (e) => initSwiper(e.target));
  document.addEventListener("htmx:afterSettle", (e) => initSwiper(e.target));
  document.addEventListener("shown.bs.modal", (e) => initSwiper(e.target));
})();
