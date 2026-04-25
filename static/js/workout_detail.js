const workoutTitle  = document.getElementById("workoutTitle");
const workoutMeta   = document.getElementById("workoutMeta");
const exerciseForm  = document.getElementById("exerciseForm");
const exercisesList = document.getElementById("exercisesList");
const messageEl     = document.getElementById("message");
const logoutBtn     = document.getElementById("logoutBtn");

const workoutId = window.location.pathname.split("/").pop();

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

async function loadWorkout() {
    const response = await fetch(`/api/workouts/${workoutId}`);

    if (response.status === 401) {
        window.location.href = "/login";
        return;
    }
    if (!response.ok) {
        workoutTitle.textContent = "Тренировка не найдена";
        return;
    }

    const workout = await response.json();
    workoutTitle.textContent = workout.title;

    workoutMeta.innerHTML = `
        <span class="meta-chip">📅 ${formatDate(workout.workout_date)}</span>
        ${workout.description ? `<span class="meta-chip">📝 ${workout.description}</span>` : ""}
        <span class="meta-chip">🏋️ ${workout.exercises ? workout.exercises.length : 0} упражнений</span>
    `;

    exercisesList.innerHTML = "";

    if (!workout.exercises || workout.exercises.length === 0) {
        exercisesList.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🏋️</div>
                <h3>Пока пусто</h3>
                <p>Добавь первое упражнение слева</p>
            </div>
        `;
        return;
    }

    workout.exercises.forEach((exercise) => {
        const setsHtml = exercise.sets && exercise.sets.length > 0
            ? `<div class="table-wrap">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Подход</th>
                            <th>Повторения</th>
                            <th>Вес, кг</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${exercise.sets.map(set => `
                            <tr>
                                <td>${set.set_number}</td>
                                <td>${set.reps}</td>
                                <td>${set.weight}</td>
                            </tr>
                        `).join("")}
                    </tbody>
                </table>
               </div>`
            : `<p class="no-sets">Подходы не добавлены</p>`;

        const card = document.createElement("div");
        card.className = "exercise-card";
        card.innerHTML = `
            <div class="exercise-card-header">
                <span class="exercise-name">${exercise.name}</span>
                <span class="badge badge-muted">${exercise.sets ? exercise.sets.length : 0} подх.</span>
            </div>
            ${exercise.description ? `<p class="exercise-desc">${exercise.description}</p>` : ""}
            ${setsHtml}
        `;
        exercisesList.appendChild(card);
    });
}

if (exerciseForm) {
    exerciseForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const response = await fetch(`/api/workouts/${workoutId}/exercises`, {
            method: "POST",
            body: new FormData(exerciseForm),
        });
        const data = await response.json();
        if (!response.ok) {
            showMessage(data.detail || "Ошибка добавления упражнения", true);
            return;
        }
        showMessage("Упражнение добавлено");
        exerciseForm.reset();
        loadWorkout();
    });
}

if (logoutBtn) {
    logoutBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        await fetch("/api/logout", { method: "POST" });
        window.location.href = "/";
    });
}

loadWorkout();