const positions = {
  P1: [7, 50],
  P2: [25, 22],
  P3: [25, 50],
  P4: [25, 78],
  P5: [39, 35],
  P6: [47, 62],
  P7: [66, 20],
  P8: [64, 50],
  P9: [84, 50],
  P10: [70, 78],
  P11: [55, 18],
};

const colors = {
  fresh: "#22c55e",
  moderate: "#eab308",
  fatigued: "#f97316",
  critical: "#ef4444",
};

const names = {
  P1: "Goalkeeper",
  P2: "Right Back",
  P3: "Centre Back",
  P4: "Centre Back",
  P5: "Left Back",
  P6: "Defensive Midfielder",
  P7: "Winger",
  P8: "Central Midfielder",
  P9: "Striker",
  P10: "Attacking Midfielder",
  P11: "Winger",
};

let selectedPlayer = null;

function seededValue(playerId, minute, offset) {
  const number = Number(playerId.replace("P", ""));
  const x = Math.sin(number * 12.9898 + minute * 0.233 + offset) * 43758.5453;
  return x - Math.floor(x);
}

function buildPrediction(playerId, minute) {
  const intensity = seededValue(playerId, minute, 4);
  const base = minute * 0.52 + intensity * 28 + (Number(playerId.replace("P", "")) % 4) * 4;
  const heat = minute > 65 ? 8 : 3;
  const score = Math.min(96, Math.max(12, Math.round(base + heat)));
  const zone = score >= 75 ? "critical" : score >= 55 ? "fatigued" : score >= 35 ? "moderate" : "fresh";
  const recommendation = score >= 75 ? "SUB NOW" : score >= 55 ? "Prepare sub" : score >= 35 ? "Watch" : "Keep";

  return {
    playerId,
    name: names[playerId],
    fatigue: score,
    energy: 100 - score,
    zone,
    recommendation,
    reasons: [
      `${minute}' cumulative load`,
      intensity > 0.55 ? "High sprint ratio" : "Stable sprint ratio",
      minute > 65 ? "Heat effort rising" : "Normal thermal stress",
    ],
  };
}

function render(minute) {
  const players = Object.keys(positions).map((id) => buildPrediction(id, minute));
  selectedPlayer = selectedPlayer || players[6];

  document.getElementById("minuteValue").textContent = `${minute}'`;
  document.getElementById("teamEnergy").textContent = `${Math.round(
    players.reduce((sum, player) => sum + player.energy, 0) / players.length
  )}%`;

  renderPitch(players);
  renderAlerts(players);
  renderDetail(players.find((player) => player.playerId === selectedPlayer.playerId) || players[0]);
}

function renderPitch(players) {
  const pitch = document.getElementById("pitch");
  pitch.querySelectorAll(".player").forEach((node) => node.remove());

  players.forEach((player) => {
    const [left, top] = positions[player.playerId];
    const node = document.createElement("button");
    node.className = "player";
    node.type = "button";
    node.style.left = `${left}%`;
    node.style.top = `${top}%`;
    node.style.background = colors[player.zone];
    node.innerHTML = `${player.playerId.replace("P", "")}<small>${player.fatigue}%</small>`;
    node.addEventListener("click", () => {
      selectedPlayer = player;
      renderDetail(player);
    });
    pitch.appendChild(node);
  });
}

function renderAlerts(players) {
  const alerts = document.getElementById("alerts");
  const risky = players.filter((player) => player.zone === "critical" || player.zone === "fatigued");

  if (risky.length === 0) {
    alerts.innerHTML = `<p class="reason">All players are currently inside safe fatigue zones.</p>`;
    return;
  }

  alerts.innerHTML = risky
    .slice(0, 4)
    .map(
      (player) => `
        <div class="alert" style="border-left-color: ${colors[player.zone]}">
          <strong>${player.playerId} - ${player.recommendation}</strong>
          <p>${player.name}: ${player.fatigue}% fatigue</p>
        </div>
      `
    )
    .join("");
}

function renderDetail(player) {
  selectedPlayer = player;
  document.getElementById("detail").innerHTML = `
    <h3>${player.playerId} - ${player.name}</h3>
    <p><strong style="color: ${colors[player.zone]}">${player.fatigue}% fatigue</strong> | ${player.energy}% energy remaining</p>
    <p>Recommendation: <strong>${player.recommendation}</strong></p>
    ${player.reasons.map((reason) => `<div class="reason">${reason}</div>`).join("")}
  `;
}

document.getElementById("minute").addEventListener("input", (event) => {
  render(Number(event.target.value));
});

render(78);

