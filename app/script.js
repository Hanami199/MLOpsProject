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

// Funzione per applicare il tema salvato
function applyTheme() {
    const theme = localStorage.getItem("theme");
    if (theme === "dark") {
        document.body.classList.add("dark");
        icon.textContent = "🌙";
    } else {
        document.body.classList.remove("dark");
        icon.textContent = "☀️";
    }
    updateLogoForTheme();
}

// Toggle e salvataggio tema
toggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    const isDark = document.body.classList.contains("dark");
    icon.textContent = isDark ? "🌙" : "☀️";
    localStorage.setItem("theme", isDark ? "dark" : "light");
    updateLogoForTheme();

});

applyTheme();
document.documentElement.classList.remove("dark-preload");

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
    const filteredMovies = movies.filter(obj => !addedMovies.has(obj.title));
    currentSuggestions = filteredMovies;

    filteredMovies.forEach((obj, idx) => {
        const { title, type } = obj;
        const li = document.createElement("li");
        li.classList.add("suggestion-item");

        // Immagine per la tendina
        const img = document.createElement("img");
        getPosterUrl(title, type).then(url => { img.src = url; });
        img.alt = title;
        img.className = "suggestion-cover";

        const span = document.createElement("span");
        span.textContent = title;
        span.className = "suggestion-title";

        li.appendChild(img);
        li.appendChild(span);

        li.addEventListener("click", () => {
            addMovieToBox(title, type);
            suggestionsList.innerHTML = "";
            movieInput.value = "";
            selectedSuggestionIndex = -1;
            currentSuggestions = [];
            updateFloatingBorder();
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
            const selectedObj = currentSuggestions[selectedSuggestionIndex];
            addMovieToBox(selectedObj.title, selectedObj.type);
            suggestionsList.innerHTML = "";
            movieInput.value = "";
            updateFloatingBorder();
            selectedSuggestionIndex = -1;
            currentSuggestions = [];
        } else if (suggestionsCount > 0) {
            e.preventDefault();
            const firstSuggestion = currentSuggestions[0];
            addMovieToBox(firstSuggestion.title, firstSuggestion.type);
            suggestionsList.innerHTML = "";
            movieInput.value = "";
            selectedSuggestionIndex = -1;
            currentSuggestions = [];
        }
    }
});

// Aggiungi film alla suggestion-box
function addMovieToBox(title, type) {
    if (addedMovies.has(title)) return; // Evita duplicati

    addedMovies.add(title);

    // Rimuovi tutti i placeholder
    suggestionBox.querySelectorAll('.suggestion-placeholder').forEach(e => e.remove());

    const div = document.createElement("div");
    div.className = "suggestion-movie";
    div.style.display = "flex";
    div.style.alignItems = "center";
    div.style.justifyContent = "space-between";
    div.style.gap = "0.7rem";

    // Copertina film per il box
    const img = document.createElement("img");
    getPosterUrl(title, type).then(url => { img.src = url; });
    img.alt = title;
    img.className = "box-cover";
    img.dataset.type = type || "movie"; // Salva il tipo nell'elemento img

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
        saveMoviesToSession();
    });

    div.appendChild(img);
    div.appendChild(span);
    div.appendChild(removeBtn);
    suggestionBox.appendChild(div);

    renderSuggestionPlaceholder();
    saveMoviesToSession();
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

document.addEventListener("DOMContentLoaded", () => {
    loadMoviesFromSession();
    renderSuggestionPlaceholder();
    updateFloatingBorder();
});

// Salva la scelta dell'algoritmo ogni volta che viene cambiata
const algoSelect = document.getElementById('algorithm');

// All'avvio, se c'è già una scelta salvata, selezionala nella tendina
const savedAlgo = sessionStorage.getItem('selectedAlgorithm');
if (savedAlgo) {
    algoSelect.value = savedAlgo;
}

// Salva la scelta dell'algoritmo ogni volta che viene cambiata
algoSelect.addEventListener('change', function() {
    sessionStorage.setItem('selectedAlgorithm', algoSelect.value);
});

document.getElementById("movieForm").addEventListener("submit", function(e) {
    e.preventDefault();
    // Se l'input è vuoto o non in focus, invia i film
    if (!movieInput.value.trim() || document.activeElement !== movieInput) {
        submitMovies();
    }
    // Altrimenti, lascia che l'input venga gestito normalmente (aggiunta film)
});

async function submitMovies() {
    const movies = Array.from(document.querySelectorAll('.suggestion-movie span'))
        .map(span => span.textContent);

    const minAlert = document.getElementById('minAlert');
    if (movies.length < 1) {
        minAlert.textContent = "Please add at least 1 movie (max 10)";
        minAlert.style.display = "block";
        setTimeout(() => { minAlert.style.display = "none"; }, 2500);
        return;
    }
    if (movies.length > 10) {
        minAlert.textContent = "You can add a maximum of 10 movies!";
        minAlert.style.display = "block";
        setTimeout(() => { minAlert.style.display = "none"; }, 2500);
        return;
    }
    minAlert.style.display = "none";

    const selectedAlgo = document.getElementById('algorithm').value;

    // Invia la richiesta al backend
    const response = await fetch('http://127.0.0.1:5000/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            algorithm: selectedAlgo,
            movies: movies
        })
    });

    const result = await response.json();
    sessionStorage.setItem('recommendedMovies', JSON.stringify(result.titles));
    sessionStorage.setItem('recommendedTypes', JSON.stringify(result.types));
    sessionStorage.setItem('selectedAlgorithm', selectedAlgo);

    window.location.href = "results.html";
}

// Permetti invio globale solo se l'input NON è in focus
document.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && document.activeElement !== movieInput) {
        e.preventDefault();
        submitMovies();
    }
});

updateFloatingBorder();
renderSuggestionPlaceholder();

function saveMoviesToSession() {
    const movies = [];
    suggestionBox.querySelectorAll('.suggestion-movie').forEach(div => {
        const span = div.querySelector('span');
        const img = div.querySelector('img');
        movies.push({ title: span.textContent, type: img.dataset.type || "movie" });
    });
    sessionStorage.setItem('suggestedMovies', JSON.stringify(movies));
}

function loadMoviesFromSession() {
    const movies = JSON.parse(sessionStorage.getItem('suggestedMovies') || "[]");
    movies.forEach(obj => {
        addMovieToBox(obj.title, obj.type);
    });
}

const selectedAlgo = document.getElementById('algorithm').value;
sessionStorage.setItem('selectedAlgorithm', selectedAlgo);

const TMDB_API_KEY = "868f9c87e383bb5a7943a5baaabc333b";

async function getPosterUrl(title, type) {
    const endpoint = tmdbType(type);
    const url = `https://api.themoviedb.org/3/search/${endpoint}?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(title)}`;
    try {
        const res = await fetch(url);
        const data = await res.json();
        if (data.results && data.results.length > 0) {
            // Cerca risultato con titolo esatto
            const exact = data.results.find(r =>
                (r.name && r.name.toLowerCase() === title.toLowerCase()) ||
                (r.title && r.title.toLowerCase() === title.toLowerCase())
            );
            const posterPath = (exact && exact.poster_path) ? exact.poster_path : data.results[0].poster_path;
            if (posterPath) {
                return `https://image.tmdb.org/t/p/w500${posterPath}`;
            }
        }
    } catch (e) {}
    return "placeholder.png";
}

async function renderResults() {
    // Recupera quanti film ha inserito l'utente
    const userMovies = JSON.parse(sessionStorage.getItem('suggestedMovies') || "[]");
    const nToShow = userMovies.length;

    // Prendi i risultati dal backend (sempre 10)
    let toDisplay = movies;

    // Se l'utente ha inserito meno di 10 film, scegli nToShow casuali tra i 10
    if (nToShow < movies.length) {
        // Shuffle e prendi i primi nToShow
        toDisplay = movies
            .map(value => ({ value, sort: Math.random() }))
            .sort((a, b) => a.sort - b.sort)
            .map(({ value }) => value)
            .slice(0, nToShow);
    }

    for (const title of toDisplay) {
        const div = document.createElement("div");
        div.className = "suggestion-movie";
        div.style.display = "flex";
        div.style.alignItems = "center";
        div.style.justifyContent = "space-between";
        div.style.gap = "0.7rem";
        div.style.marginBottom = "2rem";

        const img = document.createElement("img");
        img.src = await getPosterUrl(title);
        img.alt = title;
        img.className = "results-cover";

        const span = document.createElement("span");
        span.textContent = title;
        span.style.flex = "1";
        span.style.marginLeft = "0.5rem";

        div.appendChild(img);
        div.appendChild(span);
        resultsBox.appendChild(div);
    }
}
renderResults();

function tmdbType(type) {
    if (!type) return "movie";
    if (type.trim().toLowerCase() === "tv show") return "tv";
    return "movie";
}

function updateLogoForTheme() {
    const logoImg = document.getElementById("logo-img");
    if (!logoImg) return;
    if (document.body.classList.contains("dark")) {
        logoImg.src = "Recommendo_darktheme-removebg-preview.png";
    } else {
        logoImg.src = "Recommendo_lighttheme-removebg-preview.png";
    }
}