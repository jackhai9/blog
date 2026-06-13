(function () {
  window.blogTheme = window.blogTheme || {};
  window.blogTheme.storageKey = "blog-theme";

  window.blogTheme.getStoredTheme = function () {
    try {
      return localStorage.getItem(window.blogTheme.storageKey);
    } catch (error) {
      return null;
    }
  };

  window.blogTheme.setStoredTheme = function (theme) {
    try {
      localStorage.setItem(window.blogTheme.storageKey, theme);
    } catch (error) {
      return;
    }
  };

  window.blogTheme.prefersDark = function () {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  };

  window.blogTheme.resolve = function () {
    var savedTheme = window.blogTheme.getStoredTheme();

    if (savedTheme === "dark" || savedTheme === "light") {
      return savedTheme;
    }

    return window.blogTheme.prefersDark() ? "dark" : "light";
  };

  window.blogTheme.apply = function (theme) {
    document.documentElement.dataset.theme = theme || window.blogTheme.resolve();
  };

  window.blogTheme.apply();
})();

document.addEventListener("DOMContentLoaded", function () {
  var button = document.createElement("button");
  var icon = document.createElement("span");

  button.className = "theme-toggle";
  button.type = "button";
  icon.className = "theme-toggle-icon";
  icon.setAttribute("aria-hidden", "true");
  button.appendChild(icon);

  function renderThemeToggle() {
    var isDark = document.documentElement.dataset.theme === "dark";
    icon.textContent = isDark ? "☀" : "☾";
    button.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
    button.setAttribute("title", isDark ? "Switch to light mode" : "Switch to dark mode");
  }

  button.addEventListener("click", function () {
    var nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    window.blogTheme.apply(nextTheme);
    window.blogTheme.setStoredTheme(nextTheme);
    renderThemeToggle();
  });

  window.addEventListener("pageshow", function () {
    window.blogTheme.apply();
    renderThemeToggle();
  });

  renderThemeToggle();
  document.body.appendChild(button);
});
