// Close the navbar when clicking outside or pressing Escape
(function () {
  const navbar = document.getElementById("navbar-nav");
  const toggler = document.querySelector(".navbar-toggler");
  if (!navbar || !toggler) return;

  function hideNavbar() {
    if (!navbar.classList.contains("show")) return;
    const collapse = bootstrap.Collapse.getOrCreateInstance(navbar);
    collapse.hide();
  }
  document.addEventListener("pointerdown", (e) => {
    if (!navbar.contains(e.target) && !toggler.contains(e.target)) {
      hideNavbar();
    }
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      hideNavbar();
    }
  });
})();
