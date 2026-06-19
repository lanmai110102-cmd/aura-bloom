document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () { nav.classList.toggle("open"); });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { nav.classList.remove("open"); });
    });
  }

  // Scroll reveal
  var revealEls = document.querySelectorAll(".fade-in");
  if ("IntersectionObserver" in window && revealEls.length) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in-view"); });
  }

  // Animated counters
  var counters = document.querySelectorAll(".counter");
  if ("IntersectionObserver" in window && counters.length) {
    var counterObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        counterObserver.unobserve(el);
        var target = parseFloat(el.getAttribute("data-target")) || 0;
        var prefix = el.getAttribute("data-prefix") || "";
        var suffix = el.getAttribute("data-suffix") || "";
        var duration = 1200;
        var start = null;
        function step(timestamp) {
          if (!start) start = timestamp;
          var progress = Math.min((timestamp - start) / duration, 1);
          var value = Math.floor(progress * target);
          el.textContent = prefix + value + suffix;
          if (progress < 1) requestAnimationFrame(step);
          else el.textContent = prefix + target + suffix;
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { counterObserver.observe(el); });
  }

  var palette = ["#4c3d19", "#889063", "#cfbb99", "#354024", "#a99a7d"];

  document.querySelectorAll(".chart-canvas").forEach(function (canvas) {
    var cfg = JSON.parse(canvas.getAttribute("data-chart"));
    if (typeof Chart === "undefined") return;

    if (cfg.type === "groupedBar") {
      new Chart(canvas, {
        type: "bar",
        data: {
          labels: cfg.labels,
          datasets: cfg.datasets.map(function (ds, i) {
            return { label: ds.label, data: ds.data, backgroundColor: palette[i % palette.length], borderRadius: 6 };
          })
        },
        options: {
          responsive: true,
          plugins: { legend: { position: "bottom", labels: { font: { size: 11 } } } },
          scales: { y: { beginAtZero: true, ticks: { font: { size: 10 } } }, x: { ticks: { font: { size: 11 } } } }
        }
      });
    } else {
      new Chart(canvas, {
        type: "bar",
        data: {
          labels: cfg.labels,
          datasets: [{
            label: cfg.datasets[0].label,
            data: cfg.datasets[0].data,
            backgroundColor: cfg.labels.map(function (_, i) { return palette[i % palette.length]; }),
            borderRadius: 6
          }]
        },
        options: {
          indexAxis: cfg.labels.length <= 1 ? "y" : "x",
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true, ticks: { font: { size: 10 } } }, x: { ticks: { font: { size: 11 } } } }
        }
      });
    }
  });
});
