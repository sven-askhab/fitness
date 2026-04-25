const registerForm = document.getElementById("registerForm");
const loginForm    = document.getElementById("loginForm");
const messageEl    = document.getElementById("message");

function showMessage(text, isError = false) {
    messageEl.className = isError ? "error" : "success";
    messageEl.textContent = text;
    messageEl.style.marginBottom = "16px";
}

if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const response = await fetch("/api/register", {
            method: "POST",
            body: new FormData(registerForm),
        });
        const data = await response.json();
        if (!response.ok) {
            showMessage(data.detail || "Ошибка регистрации", true);
            return;
        }
        showMessage("Регистрация выполнена успешно");
        window.location.href = "/workouts";
    });
}

if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const response = await fetch("/api/login", {
            method: "POST",
            body: new FormData(loginForm),
        });
        const data = await response.json();
        if (!response.ok) {
            showMessage(data.detail || "Ошибка входа", true);
            return;
        }
        showMessage("Вход выполнен успешно");
        window.location.href = "/workouts";
    });
}