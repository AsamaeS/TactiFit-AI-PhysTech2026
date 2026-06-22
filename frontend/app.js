const positions = {
  P1: [7, 50],
  P2: [24, 23],
  P3: [24, 50],
  P4: [24, 77],
  P5: [40, 34],
  P6: [47, 63],
  P7: [66, 20],
  P8: [62, 50],
  P9: [84, 50],
  P10: [70, 78],
  P11: [55, 18],
};

const squad = {
  P1: ["Bounou", "GK"],
  P2: ["Hakimi", "RB"],
  P3: ["Aguerd", "CB"],
  P4: ["Saiss", "CB"],
  P5: ["Mazraoui", "LB"],
  P6: ["Amrabat", "DM"],
  P7: ["Ziyech", "RW"],
  P8: ["Ounahi", "CM"],
  P9: ["En-Nesyri", "ST"],
  P10: ["Boufal", "LW"],
  P11: ["Harit", "AM"],
};

const bench = [
  { number: 12, name: "El Kaabi", role: "ST", energy: 96, fitFor: ["P9", "P10"] },
  { number: 14, name: "Abde", role: "Winger", energy: 94, fitFor: ["P7", "P10"] },
  { number: 16, name: "Richardson", role: "Midfield", energy: 91, fitFor: ["P6", "P8", "P11"] },
  { number: 18, name: "Chibi", role: "Fullback", energy: 89, fitFor: ["P2", "P5"] },
];

const colors = {
  fresh: "#20c997",
  moderate: "#e6b800",
  fatigued: "#ff7a45",
  critical: "#f04452",
};

let selectedPlayerId = "P7";

function seededValue(playerId, minute, offset) {
  const number = Number(playerId.replace("P", ""));
  const x = Math.sin(number * 12.9898 + minute * 0.233 + offset) * 43758.5453;
  return x - Math.floor(x);
}

function zoneFor(score) {
  if (score >= 75) return "critical";
  if (score >= 55) return "fatigued";
  if (score >= 35) return "moderate";
  return "fresh";
}

function buildPrediction(playerId, minute) {
  const [name, role] = squad[playerId];
  const intensity = seededValue(playerId, minute, 4);
  const heatStress = minute > 65 ? 8 : 3;
  const roleLoad = ["RW", "LW", "ST"].includes(role) ? 8 : role === "CM" || role === "DM" ? 5 : 2;
  const base = minute * 0.5 + intensity * 28 + roleLoad;
  const fatigue = Math.min(96, Math.max(10, Math.round(base + heatStress)));
  const hrv = Math.max(24, Math.round(72 - fatigue * 0.46 + seededValue(playerId, minute, 7) * 8));
  const heartRate = Math.round(108 + fatigue * 0.92 + intensity * 16);
  const sprintLoad = Math.round(260 + fatigue * 11 + intensity * 360);
  const zone = zoneFor(fatigue);

  return {
    playerId,
    number: playerId.replace("P", ""),
    name,
    role,
    fatigue,
    energy: 100 - fatigue,
    hrv,
    heartRate,
    sprintLoad,
    zone,
    recommendation: fatigue >= 75 ? "Substitute now" : fatigue >= 55 ? "Prepare substitute" : fatigue >= 35 ? "Monitor closely" : "Keep on pitch",
    reasons: [
      { impact: Math.round(minute * 0.34), text: `${minute}' cumulative match load` },
      { impact: Math.round(intensity * 24), text: intensity > 0.55 ? "Repeated sprint exposure is high" : "Sprint exposure is controlled" },
      { impact: Math.round(Math.max(0, (60 - hrv) * 0.7)), text: "HRV trend indicates recovery pressure" },
      { impact: minute > 65 ? 11 : 4, text: "Heat and humidity add cardiovascular stress" },
    ].sort((a, b) => b.impact - a.impact),
  };
}

function bestBenchFor(player) {
  return bench
    .filter((candidate) => candidate.fitFor.includes(player.playerId))
    .sort((a, b) => b.energy - a.energy)[0] || bench[0];
}

function render(minute) {
  const players = Object.keys(positions).map((id) => buildPrediction(id, minute));
  const priority = [...players].sort((a, b) => b.fatigue - a.fatigue)[0];
  const selected = players.find((player) => player.playerId === selectedPlayerId) || priority;
  const risky = players.filter((player) => player.fatigue >= 55);
  const avgEnergy = Math.round(players.reduce((sum, player) => sum + player.energy, 0) / players.length);
  const avgHr = Math.round(players.reduce((sum, player) => sum + player.heartRate, 0) / players.length);
  const sprintLoad = Math.round(players.reduce((sum, player) => sum + player.sprintLoad, 0) / players.length);

  document.getElementById("minuteValue").textContent = `${minute}'`;
  document.getElementById("teamEnergy").textContent = `${avgEnergy}%`;
  document.getElementById("riskCount").textContent = String(risky.length);
  document.getElementById("avgHr").textContent = `${avgHr} bpm`;
  document.getElementById("sprintLoad").textContent = `${sprintLoad} m`;

  renderDecision(priority);
  renderPitch(players, selected.playerId);
  renderAlerts(players);
  renderDetail(selected);
  renderBench(priority);
}

function renderDecision(player) {
  const replacement = bestBenchFor(player);
  const arc = document.getElementById("riskArc");
  const circumference = 314;
  arc.style.strokeDashoffset = String(circumference - (circumference * player.fatigue) / 100);
  arc.style.stroke = colors[player.zone];

  document.getElementById("riskScore").textContent = `${player.fatigue}%`;
  document.getElementById("priorityTitle").textContent = `${player.name} needs attention`;
  document.getElementById("priorityCopy").textContent =
    `${player.role} is in the ${player.zone} zone with ${player.energy}% energy remaining. ${player.recommendation}.`;
  document.getElementById("swapText").textContent =
    `${replacement.name} for ${player.name} (${replacement.role}, ${replacement.energy}% ready)`;
}

function renderPitch(players, selectedId) {
  const pitch = document.getElementById("pitch");
  pitch.querySelectorAll(".player").forEach((node) => node.remove());

  players.forEach((player) => {
    const [left, top] = positions[player.playerId];
    const node = document.createElement("button");
    node.className = `player ${player.playerId === selectedId ? "is-selected" : ""}`;
    node.type = "button";
    node.style.left = `${left}%`;
    node.style.top = `${top}%`;
    node.setAttribute("aria-label", `${player.name}, ${player.fatigue}% fatigue`);
    node.innerHTML = `
      <span class="player-number" style="background:${colors[player.zone]}">${player.number}</span>
      <span class="player-score">${player.fatigue}%</span>
    `;
    node.addEventListener("click", () => {
      selectedPlayerId = player.playerId;
      render(Number(document.getElementById("minute").value));
    });
    pitch.appendChild(node);
  });
}

function renderAlerts(players) {
  const alerts = document.getElementById("alerts");
  const risky = players
    .filter((player) => player.zone === "critical" || player.zone === "fatigued")
    .sort((a, b) => b.fatigue - a.fatigue);

  if (risky.length === 0) {
    alerts.innerHTML = `<div class="alert" style="border-left-color:${colors.fresh}"><strong>Squad stable</strong><p>All players are inside safe fatigue zones.</p></div>`;
    return;
  }

  alerts.innerHTML = risky.slice(0, 4).map((player) => {
    const replacement = bestBenchFor(player);
    return `
      <button class="alert" style="border-left-color:${colors[player.zone]}" type="button" data-player="${player.playerId}">
        <strong>${player.playerId} - ${player.recommendation}</strong>
        <p>${player.name}: ${player.fatigue}% fatigue. Best bench option: ${replacement.name}.</p>
      </button>
    `;
  }).join("");

  alerts.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      selectedPlayerId = button.dataset.player;
      render(Number(document.getElementById("minute").value));
    });
  });
}

function renderDetail(player) {
  document.getElementById("detail").innerHTML = `
    <div class="detail-head">
      <div>
        <h3>${player.number}. ${player.name}</h3>
        <p>${player.role} | HR ${player.heartRate} bpm | HRV ${player.hrv} ms</p>
      </div>
      <span class="pill" style="background:${colors[player.zone]}">${player.zone}</span>
    </div>
    <p><strong style="color:${colors[player.zone]}">${player.fatigue}% fatigue</strong> with ${player.energy}% energy remaining.</p>
    ${player.reasons.map((reason) => `
      <div class="reason">
        <strong>+${reason.impact}%</strong>
        <span>${reason.text}</span>
      </div>
    `).join("")}
  `;
}

function renderBench(priority) {
  const suggested = bestBenchFor(priority);
  document.getElementById("bench").innerHTML = bench.map((player) => `
    <div class="bench-card">
      <div class="bench-no">${player.number}</div>
      <div>
        <strong>${player.name}</strong>
        <span>${player.role} | ${player.energy}% ready</span>
      </div>
      <strong>${player.name === suggested.name ? "Best" : "Ready"}</strong>
    </div>
  `).join("");
}

document.getElementById("minute").addEventListener("input", (event) => {
  render(Number(event.target.value));
});

render(78);
