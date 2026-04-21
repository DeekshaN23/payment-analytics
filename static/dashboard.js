async function loadDashboard() {
  const [summary, trend, failures] = await Promise.all([
    fetch("/api/summary").then(r => r.json()),
    fetch("/api/trend").then(r => r.json()),
    fetch("/api/failures").then(r => r.json()),
  ]);

  // KPI cards
  const total   = summary.total;
  const success = summary.by_status.find(s => s.status === "success")?.count || 0;
  const failed  = summary.by_status.find(s => s.status === "failed")?.count  || 0;
  const pending = summary.by_status.find(s => s.status === "pending")?.count || 0;

  document.getElementById("kpi-total").textContent   = total.toLocaleString();
  document.getElementById("kpi-success").textContent = ((success / total) * 100).toFixed(1) + "%";
  document.getElementById("kpi-failed").textContent  = failed.toLocaleString();
  document.getElementById("kpi-pending").textContent = pending.toLocaleString();

  // Trend chart
  new Chart(document.getElementById("trendChart"), {
    type: "line",
    data: {
      labels: trend.map(r => r.day),
      datasets: [
        { label: "Success", data: trend.map(r => r.success), borderColor: "#34d399", tension: 0.4, fill: false },
        { label: "Failed",  data: trend.map(r => r.failed),  borderColor: "#f87171", tension: 0.4, fill: false },
      ]
    },
    options: { plugins: { legend: { labels: { color: "#94a3b8" } } }, scales: { x: { ticks: { color: "#94a3b8" } }, y: { ticks: { color: "#94a3b8" } } } }
  });

  // Failure pattern chart
  new Chart(document.getElementById("failureChart"), {
    type: "bar",
    data: {
      labels: failures.map(r => r.error_code),
      datasets: [{ label: "Count", data: failures.map(r => r.count), backgroundColor: "#f87171" }]
    },
    options: { plugins: { legend: { labels: { color: "#94a3b8" } } }, scales: { x: { ticks: { color: "#94a3b8" } }, y: { ticks: { color: "#94a3b8" } } } }
  });

  loadTable();
}

async function loadTable(page = 1) {
  const status   = document.getElementById("filter-status").value;
  const category = document.getElementById("filter-category").value;
  const url      = `/api/transactions?status=${status}&category=${category}&page=${page}`;
  const rows     = await fetch(url).then(r => r.json());
  const tbody    = document.getElementById("tx-body");
  tbody.innerHTML = rows.map(r => `
    <tr>
      <td style="font-size:11px;color:#64748b">${r.id.slice(0,8)}…</td>
      <td>$${r.amount.toFixed(2)}</td>
      <td><span class="badge ${r.status}">${r.status}</span></td>
      <td>${r.category}</td>
      <td>${r.gateway}</td>
      <td style="color:#f87171">${r.error_code || "—"}</td>
      <td style="color:#64748b">${r.created_at.slice(0,10)}</td>
    </tr>
  `).join("");
}

loadDashboard();