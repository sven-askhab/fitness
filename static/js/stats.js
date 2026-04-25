const statsBlock = document.getElementById("statsBlock");
const messageEl  = document.getElementById("message");
const logoutBtn  = document.getElementById("logoutBtn");

function showMessage(text, isError = false) {
    messageEl.className = isError ? "error" : "success";
    messageEl.textContent = text;
    messageEl.style.marginBottom = "16px";
}

async function loadStats() {
    const response = await fetch("/api/stats");

    if (response.status === 401) {
        window.location.href = "/login";
        return;
    }
    if (!response.ok) {
        showMessage("Ошибка загрузки статистики", true);
        statsBlock.innerHTML = "";
        return;
    }

    const stats = await response.json();

    statsBlock.innerHTML = `
        <div class="stats-main-grid">
            <div class="stat-tile">
                <div class="stat-label">Тренировки</div>
                <div class="stat-value">${stats.total_workouts}</div>
            </div>
            <div class="stat-tile">
                <div class="stat-label">Упражнения</div>
                <div class="stat-value">${stats.total_exercises}</div>
            </div>
            <div class="stat-tile">
                <div class="stat-label">Подходы</div>
                <div class="stat-value">${stats.total_sets}</div>
            </div>
            <div class="stat-tile stat-green">
                <div class="stat-label">Повторения</div>
                <div class="stat-value">${stats.total_reps}</div>
            </div>
            <div class="stat-tile stat-accent">
                <div class="stat-label">Тренировочный объём</div>
                <div class="stat-value">${stats.total_volume} <span style="font-size:16px;font-weight:400;color:var(--text-muted)">кг</span></div>
            </div>
        </div>
    `;
}

if (logoutBtn) {
    logoutBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        await fetch("/api/logout", { method: "POST" });
        window.location.href = "/";
    });
}

loadStats();