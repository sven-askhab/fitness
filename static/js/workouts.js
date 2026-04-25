const workoutForm  = document.getElementById("workoutForm");
const workoutsList = document.getElementById("workoutsList");
const messageEl    = document.getElementById("message");
const logoutBtn    = document.getElementById("logoutBtn");

function showMessage(text, isError = false) {
    messageEl.className = isError ? "error" : "success";
    messageEl.textContent = text;
    messageEl.style.marginBottom = "16px";
}

function formatDate(dateStr) {
    if (!dateStr) return "";
    const d = new Date(dateStr);
    return d.toLocaleDateString("ru-RU", { day: "numeric", month: "long", year: "numeric" });
}

async function loadWorkouts() {
    const response = await fetch("/api/workouts");

    if (response.status === 401) {
        window.location.href = "/login";
        return;
    }

    const workouts = await response.json();
    workoutsList.innerHTML = "";

    if (workouts.length === 0) {
        workoutsList.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🗓️</div>
                <h3>Тренировок пока нет</h3>
                <p>Создай первую тренировку слева</p>
            </div>
        `;
        return;
    }

    workouts.forEach((workout) => {
        const card = document.createElement("div");
        card.className = "workout-card";
        card.innerHTML = `
            <div class="workout-card-top">
                <span class="workout-card-title">${workout.title}</span>
                <span class="badge badge-muted">${workout.exercise_count} упр.</span>
            </div>
            <div class="workout-card-meta">
                <span>📅 ${formatDate(workout.workout_date)}</span>
            </div>
            ${workout.description
                ? `<p class="workout-card-desc">${workout.description}</p>`
                : ""}
            <div class="workout-card-footer">
                <a class="btn btn-sm" href="/workouts/${workout.id}">Открыть</a>
                <button class="btn btn-sm btn-danger" onclick="deleteWorkout(${workout.id})">Удалить</button>
            </div>
        `;
        workoutsList.appendChild(card);
    });
}

if (workoutForm) {
    workoutForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const response = await fetch("/api/workouts", {
            method: "POST",
            body: new FormData(workoutForm),
        });
        const data = await response.json();
        if (!response.ok) {
            showMessage(data.detail || "Ошибка создания тренировки", true);
            return;
        }
        showMessage("Тренировка добавлена");
        workoutForm.reset();
        loadWorkouts();
    });
}

async function deleteWorkout(id) {
    if (!confirm("Удалить тренировку?")) return;
    const response = await fetch(`/api/workouts/${id}`, { method: "DELETE" });
    if (!response.ok) {
        showMessage("Ошибка удаления тренировки", true);
        return;
    }
    showMessage("Тренировка удалена");
    loadWorkouts();
}

if (logoutBtn) {
    logoutBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        await fetch("/api/logout", { method: "POST" });
        window.location.href = "/";
    });
}

loadWorkouts();