/* ===================== Debounce ===================== */
function debounce(func, delay = 400) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), delay);
    };
}

/* ===================== Elements ===================== */
const form = document.querySelector("form");
const submitBtn = form.querySelector("button[type='submit']");
const studentIdWarning = document.getElementById("studentIdWarning");
const duplicateWarning = document.getElementById("duplicateWarning");
const duplicateHelpBtn = document.getElementById("duplicateHelpBtn");
const duplicateTooltip = document.getElementById("duplicateTooltip");

const watchFields = ["student_id", "teacher", "subject", "semester", "academic_year"];

/* ===================== UI Helpers ===================== */
function highlightField(el, show) {
    if (!el) return;

    const tsControl = el.tomselect?.control;
    const select2Selection = el.nextElementSibling?.querySelector('.select2-selection');
    const target = tsControl || select2Selection || el;

    if (show) {
        target.classList.add("border-red-500");
        target.classList.remove("border-gray-300", "dark:border-gray-600");
    } else {
        target.classList.remove("border-red-500");
        target.classList.add("border-gray-300", "dark:border-gray-600");
    }
}

function setSubmitDisabled(disabled) {
    submitBtn.disabled = disabled;
    submitBtn.classList.toggle("opacity-50", disabled);
    submitBtn.classList.toggle("cursor-not-allowed", disabled);
}

/* ===================== Warnings ===================== */
function showStudentIdWarning(show) {
    if (!studentIdWarning) return;
    studentIdWarning.classList.toggle("hidden", !show);
    highlightField(form["student_id"], show);
}

function showDuplicateWarning(show) {
    if (!duplicateWarning) return;
    duplicateWarning.classList.toggle("hidden", !show);
    watchFields.forEach(name => highlightField(form[name], show));
}

/* ===================== Validation ===================== */
async function validateEvaluation() {
    const params = new URLSearchParams();

    watchFields.forEach(name => {
        const val = form[name]?.value.trim();
        if (val) params.append(name, val);
    });

    // Reset if no Student ID
    if (!params.get("student_id") || !navigator.onLine) {
        showStudentIdWarning(false);
        showDuplicateWarning(false);
        setSubmitDisabled(false);
        return;
    }

    try {
        const res = await fetch(`/validate-evaluation/?${params}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });
        const data = await res.json();

        // Show/hide warnings
        const invalidId = !data.student_exists;
        const duplicate = data.duplicate;

        showStudentIdWarning(invalidId);
        showDuplicateWarning(duplicate);

        // Disable submit if either invalid ID or duplicate exists
        setSubmitDisabled(invalidId || duplicate);

    } catch (err) {
        console.error("Validation error:", err);
        showStudentIdWarning(false);
        showDuplicateWarning(false);
        setSubmitDisabled(false);
    }
}

/* ===================== Event Listeners ===================== */
// Real-time Student ID validation
form["student_id"].addEventListener("input", debounce(validateEvaluation, 400));
form["student_id"].addEventListener("change", validateEvaluation);

// Watch other fields for duplicate evaluation
watchFields.forEach(name => {
    if (name === "student_id") return;
    const el = form[name];
    if (!el) return;
    el.addEventListener("input", debounce(validateEvaluation, 500));
    el.addEventListener("change", debounce(validateEvaluation, 500));
});

/* ===================== Duplicate Tooltip ===================== */
if (duplicateHelpBtn && duplicateTooltip) {
    duplicateHelpBtn.addEventListener("click", e => {
        e.stopPropagation();
        duplicateTooltip.classList.toggle("hidden");
    });

    document.addEventListener("click", e => {
        if (!duplicateTooltip.contains(e.target) && e.target !== duplicateHelpBtn) {
            duplicateTooltip.classList.add("hidden");
        }
    });
}

/* ===================== Dark Mode Toggle ===================== */
function toggleDarkMode() {
    document.documentElement.classList.toggle('dark');
}

/* ===================== TomSelect Teacher Select ===================== */
// Uncomment if using TomSelect
/*
new TomSelect("#teacherSelect", {
    maxItems: 1,
    valueField: "id",
    labelField: "name",
    searchField: "name",
    load: function(query, callback) {
        const url = this.input.getAttribute("data-ajax-url") + "?q=" + encodeURIComponent(query);
        fetch(url)
            .then(res => res.json())
            .then(json => callback(json))
            .catch(() => callback());
    }
});
*/