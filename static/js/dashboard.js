const form = document.getElementById("upload-form");
const fileInput = document.getElementById("file-input");
const statusEl = document.getElementById("status");
const exportLink = document.getElementById("export-link");

let cohortChart;
let trendChart;
let segmentChart;

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.className = isError ? "text-danger small mt-3" : "text-success small mt-3";
}

function updateSummary(summary) {
  document.getElementById("total-customers").textContent = summary.total_customers;
  document.getElementById("churn-rate").textContent = `${summary.churn_rate}%`;
  document.getElementById("retention-rate").textContent = `${summary.retention_rate}%`;
  document.getElementById("avg-tenure").textContent = summary.average_tenure_days;
}

function renderChart(target, config, existing) {
  if (existing) {
    existing.destroy();
  }
  return new Chart(target, config);
}

async function loadAnalytics() {
  const [cohortsRes, trendsRes, segmentsRes] = await Promise.all([
    fetch("/api/cohorts"),
    fetch("/api/trends"),
    fetch("/api/segments"),
  ]);

  const cohorts = await cohortsRes.json();
  const trends = await trendsRes.json();
  const segments = await segmentsRes.json();

  cohortChart = renderChart(document.getElementById("cohortChart"), {
    type: "bar",
    data: {
      labels: cohorts.map((item) => item.cohort_month),
      datasets: [{ label: "Churn Rate %", data: cohorts.map((item) => item.churn_rate), backgroundColor: "#0d6efd" }],
    },
    options: { responsive: true, maintainAspectRatio: false },
  }, cohortChart);

  trendChart = renderChart(document.getElementById("trendChart"), {
    type: "line",
    data: {
      labels: trends.map((item) => item.activity_month),
      datasets: [{ label: "Churn Rate %", data: trends.map((item) => item.churn_rate), borderColor: "#dc3545", tension: 0.2 }],
    },
    options: { responsive: true, maintainAspectRatio: false },
  }, trendChart);

  const planSegments = segments.plan || [];
  segmentChart = renderChart(document.getElementById("segmentChart"), {
    type: "bar",
    data: {
      labels: planSegments.map((item) => item.plan),
      datasets: [{ label: "Churn Rate %", data: planSegments.map((item) => item.churn_rate), backgroundColor: "#198754" }],
    },
    options: { responsive: true, maintainAspectRatio: false },
  }, segmentChart);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const file = fileInput.files[0];
  if (!file) {
    setStatus("Please select a CSV file first.", true);
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  setStatus("Uploading and processing...");

  const response = await fetch("/api/upload", {
    method: "POST",
    body: formData,
  });

  const payload = await response.json();

  if (!response.ok) {
    setStatus(payload.error || "Upload failed.", true);
    return;
  }

  updateSummary(payload.summary);
  await loadAnalytics();
  exportLink.classList.remove("d-none");
  setStatus("Dataset processed successfully.");
});
