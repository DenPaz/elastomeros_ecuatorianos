// Hide the navbar when clicking outside of it or pressing Escape
(function () {
  const navbar = document.getElementById("navbarNav");
  const toggler = document.querySelector(".navbar-toggler");
  if (!navbar || !toggler) return;

  function hideNavbar() {
    if (!navbar.classList.contains("show")) return;
    const bsCollapse = bootstrap.Collapse.getOrCreateInstance(navbar);
    bsCollapse.hide();
  }

  document.addEventListener("pointerdown", (event) => {
    if (!navbar.contains(event.target) && !toggler.contains(event.target)) {
      hideNavbar();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      hideNavbar();
    }
  });
})();

/* Toast messages — server-rendered + HTMX HX-Trigger */
(function () {
  function escapeHtml(text) {
    var div = document.createElement("div");
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  function initToast(el) {
    var delay = parseInt(el.getAttribute("data-bs-delay") || "2000", 10);
    var timeoutId = null;
    var bar = el.querySelector(".timer-bar");
    var controller = new AbortController();
    var signal = controller.signal;

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
        if (bar) {
          bar.style.animation = "none";
          bar.offsetHeight;
          bar.style.animation = "";
        }
        start(delay);
      },
      { signal: signal },
    );

    el.addEventListener(
      "hidden.bs.toast",
      function () {
        clearTimeout(timeoutId);
        controller.abort();
        el.remove();
      },
      { signal: signal },
    );

    el.addEventListener(
      "mouseenter",
      function () {
        pause();
      },
      { signal: signal },
    );

    el.addEventListener(
      "mouseleave",
      function () {
        if (bar) {
          bar.style.animation = "none";
          bar.offsetHeight;
          bar.style.animation = "";
          bar.style.animationPlayState = "running";
        }
        start(delay);
      },
      { signal: signal },
    );

    new bootstrap.Toast(el).show();
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("#toast-container .toast").forEach(initToast);
  });

  document.body.addEventListener("messages", function (event) {
    var container = document.getElementById("toast-container");
    var messages = event.detail.value || event.detail;

    messages.forEach(function (msg) {
      var level = msg.tags || "info";
      var el = document.createElement("div");
      el.className = "toast fade text-bg-" + level;
      el.setAttribute("role", "alert");
      el.setAttribute("aria-live", "assertive");
      el.setAttribute("aria-atomic", "true");
      el.setAttribute("data-bs-autohide", "false");
      el.setAttribute("data-bs-delay", "2000");
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
