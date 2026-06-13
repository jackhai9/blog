(function () {
  window.blogTheme = window.blogTheme || {};
  window.blogTheme.legacyStorageKeys = ["blog-theme", "blog-theme-override"];
  window.blogTheme.storageKey = "blog-theme-mode";
  window.blogTheme.systemThemeQuery = window.matchMedia
    ? window.matchMedia("(prefers-color-scheme: dark)")
    : null;

  window.blogTheme.clearLegacyStoredThemes = function () {
    window.blogTheme.legacyStorageKeys.forEach(function (storageKey) {
      try {
        localStorage.removeItem(storageKey);
      } catch (error) {
        return;
      }
    });
  };

  window.blogTheme.getStoredMode = function () {
    try {
      var storedMode = localStorage.getItem(window.blogTheme.storageKey);

      if (storedMode === "light" || storedMode === "dark") {
        return storedMode;
      }
    } catch (error) {
      return "system";
    }

    return "system";
  };

  window.blogTheme.setStoredMode = function (mode) {
    try {
      if (mode === "system") {
        localStorage.removeItem(window.blogTheme.storageKey);
        return;
      }

      localStorage.setItem(window.blogTheme.storageKey, mode);
    } catch (error) {
      return;
    }
  };

  window.blogTheme.prefersDark = function () {
    return window.blogTheme.systemThemeQuery && window.blogTheme.systemThemeQuery.matches;
  };

  window.blogTheme.resolveTheme = function (mode) {
    var resolvedMode = mode || window.blogTheme.getStoredMode();

    if (resolvedMode === "light" || resolvedMode === "dark") {
      return resolvedMode;
    }

    return window.blogTheme.prefersDark() ? "dark" : "light";
  };

  window.blogTheme.apply = function (mode) {
    var resolvedMode = mode || window.blogTheme.getStoredMode();

    document.documentElement.dataset.themeMode = resolvedMode;
    document.documentElement.dataset.theme = window.blogTheme.resolveTheme(resolvedMode);
  };

  window.blogTheme.nextMode = function () {
    var currentMode = window.blogTheme.getStoredMode();

    if (currentMode === "system") {
      return "light";
    }

    if (currentMode === "light") {
      return "dark";
    }

    return "system";
  };

  window.blogTheme.handleSystemThemeChange = function () {
    if (window.blogTheme.getStoredMode() !== "system") {
      return;
    }

    window.blogTheme.apply("system");

    if (window.blogTheme.renderToggle) {
      window.blogTheme.renderToggle();
    }
  };

  window.blogTheme.watchSystemTheme = function () {
    var query = window.blogTheme.systemThemeQuery;

    if (!query) {
      return;
    }

    if (query.addEventListener) {
      query.addEventListener("change", window.blogTheme.handleSystemThemeChange);
      return;
    }

    if (query.addListener) {
      query.addListener(window.blogTheme.handleSystemThemeChange);
    }
  };

  window.blogTheme.clearLegacyStoredThemes();
  window.blogTheme.watchSystemTheme();
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

  window.blogTheme.renderToggle = function () {
    var mode = window.blogTheme.getStoredMode();
    var nextMode = window.blogTheme.nextMode();
    var labels = {
      system: "System",
      light: "Light",
      dark: "Dark",
    };
    var icons = {
      system: "◐",
      light: "☀",
      dark: "☾",
    };

    icon.textContent = icons[mode];
    button.setAttribute("aria-label", "Theme mode: " + labels[mode] + ". Switch to " + labels[nextMode].toLowerCase() + " mode");
    button.setAttribute("title", "Theme mode: " + labels[mode] + ". Switch to " + labels[nextMode].toLowerCase() + " mode");
  };

  button.addEventListener("click", function () {
    var nextMode = window.blogTheme.nextMode();

    window.blogTheme.setStoredMode(nextMode);
    window.blogTheme.apply(nextMode);
    window.blogTheme.renderToggle();
  });

  window.addEventListener("pageshow", function () {
    window.blogTheme.apply();
    window.blogTheme.renderToggle();
  });

  window.blogTheme.renderToggle();
  document.body.appendChild(button);
});
