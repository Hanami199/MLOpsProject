const toggle = document.getElementById("toggleSwitch");
const icon = document.querySelector(".icon");
const movieInput = document.getElementById("movieInput");
const suggestionsList = document.getElementById("suggestions");
const suggestionBox = document.getElementById("suggestionBox");

toggle.addEventListener("click", ()=>{
    document.body.classList.toggle("dark");
    icon.textContent = document.body.classList.contains("dark") ? "🌙" : "☀️";
});

// Funzione per mostrare suggerimenti
movieInput.addEventListener("input", async function() {
    const query = movieInput.value.trim();
    suggestionsList.innerHTML = "";
    if (query.length < 2) return;

    // Cambia l'URL se il backend è su un'altra porta
    const res = await fetch(`http://127.0.0.1:5000/movies?query=${encodeURIComponent(query)}`);
    const movies = await res.json();

    movies.forEach(title => {
        const li = document.createElement("li");
        li.textContent = title;
        li.addEventListener("click", () => {
            addMovieToBox(title);
            suggestionsList.innerHTML = "";
            movieInput.value = "";
        });
        suggestionsList.appendChild(li);
    });
});

// Aggiungi film alla suggestion-box
function addMovieToBox(title) {
    const div = document.createElement("div");
    div.textContent = title;
    suggestionBox.appendChild(div);
}

// Nascondi suggerimenti quando si clicca fuori
document.addEventListener("click", (e) => {
    if (!movieInput.contains(e.target) && !suggestionsList.contains(e.target)) {
        suggestionsList.innerHTML = "";
    }
});