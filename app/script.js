const toggle = document.getElementById("toggleSwitch");
const icon = document.querySelector(".icon");
const movieInput = document.getElementById("movieInput");
const suggestionsList = document.getElementById("suggestions");
const suggestionBox = document.getElementById("suggestionBox");
const inputWrapper = document.querySelector('.input-wrapper');
let selectedSuggestionIndex = -1;
let currentSuggestions = [];

// Mantieni una lista dei film già aggiunti
const addedMovies = new Set();

toggle.addEventListener("click", ()=>{
    document.body.classList.toggle("dark");
    icon.textContent = document.body.classList.contains("dark") ? "🌙" : "☀️";
});

// Funzione per mostrare suggerimenti
movieInput.addEventListener("input", async function() {
    const query = movieInput.value.trim();
    suggestionsList.innerHTML = "";
    selectedSuggestionIndex = -1;
    currentSuggestions = [];
    if (query.length < 2) return;

    const res = await fetch(`http://127.0.0.1:5000/movies?query=${encodeURIComponent(query)}`);
    const movies = await res.json();

    // Filtra i film già aggiunti
    const filteredMovies = movies.filter(title => !addedMovies.has(title));
    currentSuggestions = filteredMovies;

    filteredMovies.forEach((title, idx) => {
        const li = document.createElement("li");
        li.classList.add("suggestion-item");

        // Immagine per la tendina
        const img = document.createElement("img");
        img.src = "placeholder.png";
        img.alt = title;
        img.className = "suggestion-cover"; // <-- classe per la tendina

        const span = document.createElement("span");
        span.textContent = title;
        span.className = "suggestion-title";

        li.appendChild(img);
        li.appendChild(span);

        li.addEventListener("click", () => {
            addMovieToBox(title);
            suggestionsList.innerHTML = "";
            movieInput.value = "";
            selectedSuggestionIndex = -1;
            currentSuggestions = [];
            updateFloatingBorder(); // <-- AGGIUNGI QUESTA RIGA
        });
        suggestionsList.appendChild(li);
    });
});

movieInput.addEventListener("keydown", function(e) {
    const suggestionsCount = suggestionsList.children.length;
    if (suggestionsCount === 0) return;

    if (e.key === "ArrowDown") {
        e.preventDefault();
        selectedSuggestionIndex = (selectedSuggestionIndex + 1) % suggestionsCount;
        updateSuggestionHighlight();
    } else if (e.key === "ArrowUp") {
        e.preventDefault();
        selectedSuggestionIndex = (selectedSuggestionIndex - 1 + suggestionsCount) % suggestionsCount;
        updateSuggestionHighlight();
    } else if (e.key === "Enter") {
        if (selectedSuggestionIndex >= 0 && selectedSuggestionIndex < suggestionsCount) {
            e.preventDefault();
            const selectedTitle = currentSuggestions[selectedSuggestionIndex];
            addMovieToBox(selectedTitle);
            suggestionsList.innerHTML = "";
            movieInput.value = "";
            updateFloatingBorder();
            selectedSuggestionIndex = -1;
            currentSuggestions = [];
        } else if (suggestionsCount > 0) {
            e.preventDefault();
            const firstSuggestion = suggestionsList.children[0];
            if (firstSuggestion) {
                addMovieToBox(firstSuggestion.textContent);
                suggestionsList.innerHTML = "";
                movieInput.value = "";
                selectedSuggestionIndex = -1;
                currentSuggestions = [];
            }
        }
    }
});

// Aggiungi film alla suggestion-box
function addMovieToBox(title) {
    if (addedMovies.has(title)) return; // Evita duplicati

    addedMovies.add(title);

    // Rimuovi tutti i placeholder
    suggestionBox.querySelectorAll('.suggestion-placeholder').forEach(e => e.remove());

    const div = document.createElement("div");
    div.className = "suggestion-movie"; // <--- AGGIUNGI QUESTA CLASSE
    div.style.display = "flex";
    div.style.alignItems = "center";
    div.style.justifyContent = "space-between";
    div.style.gap = "0.7rem";

    // Copertina film per il box
    const img = document.createElement("img");
    img.src = "placeholder.png";
    img.alt = title;
    img.className = "box-cover";

    const span = document.createElement("span");
    span.textContent = title;
    span.style.flex = "1";
    span.style.marginLeft = "0.5rem";

    const removeBtn = document.createElement("button");
    removeBtn.innerHTML = "🗑️";
    removeBtn.title = "Remove";
    removeBtn.style.marginLeft = "12px";
    removeBtn.style.background = "none";
    removeBtn.style.border = "none";
    removeBtn.style.cursor = "pointer";
    removeBtn.style.fontSize = "18px";
    removeBtn.addEventListener("click", () => {
        div.remove();
        addedMovies.delete(title);
        renderSuggestionPlaceholder();
    });

    div.appendChild(img);
    div.appendChild(span);
    div.appendChild(removeBtn);
    suggestionBox.appendChild(div);

    renderSuggestionPlaceholder();
}

// Nascondi suggerimenti quando si clicca fuori
document.addEventListener("click", (e) => {
    if (!movieInput.contains(e.target) && !suggestionsList.contains(e.target)) {
        suggestionsList.innerHTML = "";
    }
});

function updateSuggestionHighlight() {
    Array.from(suggestionsList.children).forEach((li, idx) => {
        if (idx === selectedSuggestionIndex) {
            li.style.background = "#bde4ff";
            // Fai scrollare l'elemento selezionato nella vista
            li.scrollIntoView({ block: "nearest" });
        } else {
            li.style.background = "";
        }
    });
}

movieInput.addEventListener('input', updateFloatingBorder);
movieInput.addEventListener('focus', updateFloatingBorder);
movieInput.addEventListener('blur', updateFloatingBorder);

function updateFloatingBorder() {
    if (movieInput.value || document.activeElement === movieInput) {
        inputWrapper.classList.add('label-floating');
    } else {
        inputWrapper.classList.remove('label-floating');
    }
}

// Funzione per il segnaposto
function renderSuggestionPlaceholder() {
    // Rimuovi tutti i placeholder
    suggestionBox.querySelectorAll('.suggestion-placeholder').forEach(e => e.remove());

    // Conta quanti film sono presenti
    const movieCount = suggestionBox.querySelectorAll('div:not(.suggestion-placeholder)').length;

    // Aggiungi placeholder solo se meno di 5 film
    if (movieCount < 5) {
        for (let i = movieCount; i < 5; i++) {
            const placeholder = document.createElement('div');
            placeholder.className = 'suggestion-placeholder';
            placeholder.textContent = "Add a movie";
            suggestionBox.appendChild(placeholder);
        }
    }
}

document.addEventListener("DOMContentLoaded", renderSuggestionPlaceholder);

updateFloatingBorder();
renderSuggestionPlaceholder();