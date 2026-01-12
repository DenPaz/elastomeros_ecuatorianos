// Hide the navbar when clicking outside of it or pressing Escape
(function () {
  const navbar = document.getElementById("navbar-nav");
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
