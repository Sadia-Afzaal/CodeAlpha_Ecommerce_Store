(function () {
  "use strict";

  function getCookie(name) {
    const m = document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)");
    return m ? m.pop() : "";
  }
  const csrftoken = getCookie("csrftoken");

  function showToast(msg, type) {
    let wrap = document.querySelector(".toast-wrap");
    if (!wrap) {
      wrap = document.createElement("div");
      wrap.className = "container toast-wrap";
      document.body.appendChild(wrap);
    }
    const t = document.createElement("div");
    t.className = "toast toast--" + (type || "success");
    t.textContent = msg;
    wrap.appendChild(t);
    setTimeout(() => t.remove(), 4000);
  }

  function updateCartCount(count) {
    document.querySelectorAll("[data-cart-count]").forEach((el) => {
      el.textContent = count;
      el.hidden = count === 0;
    });
  }

  // AJAX add-to-cart (used by product cards) ------------------------------
  document.addEventListener("submit", function (e) {
    const form = e.target.closest("form[data-ajax-add]");
    if (!form) return;
    e.preventDefault();
    const url = form.getAttribute("action");
    const data = new FormData(form);
    fetch(url, {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": csrftoken },
      body: data,
    })
      .then((r) => r.json())
      .then((json) => {
        if (json.ok) {
          updateCartCount(json.count);
          const name = form.getAttribute("data-name") || "Item";
          showToast("Added “" + name + "” to your cart", "success");
          const btn = form.querySelector("button");
          if (btn) {
            const original = btn.innerHTML;
            btn.innerHTML = "✓";
            btn.classList.add("is-added");
            setTimeout(() => {
              btn.innerHTML = original;
              btn.classList.remove("is-added");
            }, 1200);
          }
        }
      })
      .catch(() => showToast("Something went wrong", "error"));
  });

  // Quantity steppers -----------------------------------------------------
  document.addEventListener("click", function (e) {
    const step = e.target.closest("[data-step]");
    if (!step) return;
    const input = step.parentElement.querySelector("input");
    if (!input) return;
    const dir = parseInt(step.getAttribute("data-step"), 10);
    const max = parseInt(input.getAttribute("max"), 10) || 99;
    let val = parseInt(input.value, 10) || 1;
    val = Math.min(max, Math.max(1, val + dir));
    input.value = val;
    input.dispatchEvent(new Event("change", { bubbles: true }));
  });

  // Sort dropdown on shop page -------------------------------------------
  const sortSelect = document.querySelector("[data-sort]");
  if (sortSelect) {
    sortSelect.addEventListener("change", function () {
      const url = new URL(window.location.href);
      if (this.value) url.searchParams.set("sort", this.value);
      else url.searchParams.delete("sort");
      url.searchParams.delete("page");
      window.location.href = url.toString();
    });
  }

  // Wishlist toggle (local, cosmetic) ------------------------------------
  const WISH_KEY = "aurora_wishlist";
  function getWishlist() {
    try {
      return JSON.parse(localStorage.getItem(WISH_KEY) || "[]");
    } catch (_) {
      return [];
    }
  }
  function renderWishlist() {
    const list = getWishlist();
    document.querySelectorAll("[data-fav]").forEach((b) => {
      b.classList.toggle("is-active", list.includes(b.getAttribute("data-fav")));
    });
  }
  document.addEventListener("click", function (e) {
    const fav = e.target.closest("[data-fav]");
    if (!fav) return;
    e.preventDefault();
    const id = fav.getAttribute("data-fav");
    let list = getWishlist();
    if (list.includes(id)) list = list.filter((x) => x !== id);
    else list.push(id);
    localStorage.setItem(WISH_KEY, JSON.stringify(list));
    renderWishlist();
  });
  renderWishlist();

  // Header shadow on scroll ----------------------------------------------
  const header = document.getElementById("site-header");
  if (header) {
    const onScroll = () =>
      header.style.setProperty(
        "box-shadow",
        window.scrollY > 8 ? "var(--shadow-sm)" : "none"
      );
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
})();
