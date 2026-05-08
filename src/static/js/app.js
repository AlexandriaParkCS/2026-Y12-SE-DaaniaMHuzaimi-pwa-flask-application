if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("static/js/serviceWorker.js")
      .then((res) => console.log("service worker registered"))
      .catch((err) => console.log("service worker not registered", err));
  });
}

// This script toggles the active class and aria-current attribute on the nav links
document.addEventListener("DOMContentLoaded", function () {
  var navLinks = document.querySelectorAll(".nav-link");
  var currentUrl = window.location.pathname;

  for (var i = 0; i < navLinks.length; i++) {
    var link = navLinks[i];
    var linkUrl = link.getAttribute("href");
    if (linkUrl === currentUrl) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    } else {
      link.classList.remove("active");
      link.removeAttribute("aria-current");
    }
  }

  // -- Theme toggle (dark / light / purple) --
  var htmlTag = document.documentElement;
  var toggleButton = document.getElementById("themeToggle");
  var metaTheme = document.querySelector('meta[name="theme-color"]');

  // Stop here if the button was not found
  if (toggleButton === null) {
    return;
  }

  // Load the saved theme, or start with dark
  var currentTheme = localStorage.getItem("theme");
  if (currentTheme === null) {
    currentTheme = "dark";
  }

  // Apply the loaded theme to the page
  applyTheme(currentTheme);

  // When the user clicks the theme button
  toggleButton.addEventListener("click", function () {
    // Cycle: dark -> light -> purple -> dark
    if (currentTheme === "dark") {
      currentTheme = "light";
    } else if (currentTheme === "light") {
      currentTheme = "purple";
    } else {
      currentTheme = "dark";
    }

    // Save choice and update the pagel
    localStorage.setItem("theme", currentTheme);
    applyTheme(currentTheme);
  });

  // This function switches all theme-related things at once
  function applyTheme(theme) {

    // 1. Update the data-theme attribute on <html>
    htmlTag.setAttribute("data-theme", theme);

    // 2. Change the button icon and tooltip text
    if (theme === "dark") {
      toggleButton.innerHTML = "🌙";
      toggleButton.title = "Theme: Dark";
    } else if (theme === "light") {
      toggleButton.innerHTML ="☀️";
      toggleButton.title = "Theme: Light";
    } else if (theme === "purple") {
      toggleButton.innerHTML = "💜";
      toggleButton.title = "Theme: Purple";

    }

    // 3. Update the browser address bar colour
    if (metaTheme !== null) {
      if (theme === "dark") {
        metaTheme.setAttribute("content", "#1a1040");
      } else if (theme === "light") {
        metaTheme.setAttribute("content", "#6366f1");
      } else if (theme === "purple") {
        metaTheme.setAttribute("content", "#2d1040");
      }
    }
  }
});
