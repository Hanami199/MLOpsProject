// Recupera i film dalla sessionStorage
        const movies = JSON.parse(sessionStorage.getItem('recommendedMovies') || "[]");
        const detailsArr = JSON.parse(sessionStorage.getItem('recommendedDetails') || "[]");
        const resultsBox = document.getElementById('resultsBox');
        const list = document.getElementById('movieList');
        list.style.display = "none";

        // Pop-up container
        const popup = document.createElement("div");
        popup.className = "movie-popup";
        popup.style.display = "none";
        document.body.appendChild(popup);

        let popupLocked = false;
        let lockedMovieDiv = null;

        let selectedIndex = -1;
        let movieDivs = [];

        function showPopup(imgSrc, title, description, anchorDiv, details) {
            const rating = details?.rating || "-";
            const releaseYear = details?.release_year || "-";
            const duration = details?.duration || "-";
            const listedIn = details?.listed_in || "-";

            popup.innerHTML = `
                <img src="${imgSrc}" alt="${title}" class="popup-cover" />
                <div class="popup-info">
                    <div class="popup-title">${title}</div>
                    <div class="popup-meta">
                        <span><strong>Rating:</strong> ${rating}</span> &nbsp;|&nbsp;
                        <span><strong>Year:</strong> ${releaseYear}</span> &nbsp;|&nbsp;
                        <span><strong>Duration:</strong> ${duration}</span>
                    </div>
                    <div class="popup-genre">
                        <strong>Genre:</strong> ${listedIn}
                    </div>
                    <div class="popup-desc">${description}</div>
                </div>
            `;
            popup.style.position = "fixed";
            popup.style.display = "flex";
            popup.style.visibility = "visible";
            popup.style.animation = "none";

            const filmRect = anchorDiv.getBoundingClientRect();
            const popupWidth = popup.offsetWidth;
            const left = window.innerWidth / 2 + 200 - popupWidth / 2;
            popup.style.left = `${left}px`;
            popup.style.top = `${filmRect.top + filmRect.height / 2}px`;
            popup.style.transform = "translateY(-50%)";

            void popup.offsetWidth;
            popup.style.animation = "fadeIn 0.18s";
        }

        function hidePopup() {
            if (!popupLocked) {
                popup.style.display = "none";
                popup.style.visibility = "hidden";
                lockedMovieDiv = null;
            }
        }

        // Inserisci la tua API key qui
        const TMDB_API_KEY = "868f9c87e383bb5a7943a5baaabc333b";

        // Funzione per ottenere la copertina da TMDb
        async function getPosterUrl(title, type) {
            let endpoint = "movie";
            if (type && type.toLowerCase() === "tv show") endpoint = "tv";
            const url = `https://api.themoviedb.org/3/search/${endpoint}?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(title)}`;
            try {
                const res = await fetch(url);
                const data = await res.json();
                if (data.results && data.results.length > 0 && data.results[0].poster_path) {
                    return `https://image.tmdb.org/t/p/w500${data.results[0].poster_path}`;
                }
            } catch (e) {}
            return "placeholder.png";
        }

        async function getDescription(title, type) {
            try {
                const endpoint = (type && type.toLowerCase() === "tv show") ? "tv" : "movie";
                const url = `https://api.themoviedb.org/3/search/${endpoint}?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(title)}`;
                const res = await fetch(url);
                const data = await res.json();
                if (data.results && data.results.length > 0 && data.results[0].overview) {
                    return data.results[0].overview;
                }
            } catch (e) {}
            return "";
        }

        async function renderResults() {
            // Quanti film ha inserito l'utente?
            const userMovies = JSON.parse(sessionStorage.getItem('suggestedMovies') || "[]");
            const nToShow = userMovies.length;

            // Prendi i risultati dal backend (sempre 10)
            let toDisplay = [];

            if (nToShow === 1) {
                toDisplay = [movies[0]];
            } else if (nToShow === 2) {
                toDisplay = movies.slice(0, 2);
            } else if (nToShow > 2) {
                // Prendi i primi 2 suggeriti
                const firstTwo = movies.slice(0, 2);
                // Prendi i restanti (escludendo i primi 2)
                const rest = movies.slice(2);
                // Mischia i restanti e prendine nToShow-2
                const shuffled = rest
                    .map(value => ({ value, sort: Math.random() }))
                    .sort((a, b) => a.sort - b.sort)
                    .map(({ value }) => value)
                    .slice(0, nToShow - 2);
                toDisplay = firstTwo.concat(shuffled);
            }

            for (let i = 0; i < toDisplay.length; i++) {
                const title = toDisplay[i];
                // Trova l'indice del titolo in movies
                const idx = movies.indexOf(title);
                const details = detailsArr[idx] || {};
                const type = details.type || "movie";

                const div = document.createElement("div");
                div.className = "suggestion-movie";
                div.style.display = "flex";
                div.style.alignItems = "center";
                div.style.justifyContent = "space-between";
                div.style.gap = "0.7rem";
                div.style.marginBottom = "2rem";

                const img = document.createElement("img");
                img.src = await getPosterUrl(title, type);
                img.alt = title;
                img.className = "results-cover";

                const span = document.createElement("span");
                span.textContent = title;
                span.style.flex = "1";
                span.style.marginLeft = "0.5rem";

                // Recupera la descrizione da TMDb
                let description = "";
                try {
                    const endpoint = (type && type.toLowerCase() === "tv show") ? "tv" : "movie";
                    const url = `https://api.themoviedb.org/3/search/${endpoint}?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(title)}`;
                    const res = await fetch(url);
                    const data = await res.json();
                    if (data.results && data.results.length > 0 && data.results[0].overview) {
                        description = data.results[0].overview;
                    }
                } catch (e) {}

                // Mostra pop-up su hover/click
                div.addEventListener("mouseenter", () => {
                    if (!popupLocked) showPopup(img.src, title, description, div, details);
                });
                div.addEventListener("mouseleave", () => {
                    if (!popupLocked) hidePopup();
                });
                div.addEventListener("click", () => {
                    if (popupLocked && lockedMovieDiv === div) {
                        popupLocked = false;
                        lockedMovieDiv = null;
                        hidePopup();
                    } else {
                        popupLocked = true;
                        lockedMovieDiv = div;
                        showPopup(img.src, title, description, div, details);
                    }
                });

                div.appendChild(img);
                div.appendChild(span);
                resultsBox.appendChild(div);
                movieDivs.push(div);
            }
        }
        renderResults();

        // Se clicchi fuori dal popup e da ogni film, sblocca e nascondi il popup
        document.addEventListener("click", function(e) {
            if (
                popupLocked &&
                !popup.contains(e.target) &&
                !e.target.classList.contains("suggestion-movie") &&
                !e.target.classList.contains("results-cover")
            ) {
                popupLocked = false;
                lockedMovieDiv = null;
                hidePopup();
            }
        });

        // Tema toggle con persistenza
        const toggle = document.getElementById("toggleSwitch");
        const icon = document.querySelector(".icon");
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
        toggle.addEventListener("click", () => {
            document.body.classList.toggle("dark");
            const isDark = document.body.classList.contains("dark");
            icon.textContent = isDark ? "🌙" : "☀️";
            localStorage.setItem("theme", isDark ? "dark" : "light");
            updateLogoForTheme();
        });
        applyTheme();
        document.documentElement.classList.remove("dark-preload");

        // Pulsante "Back" per tornare all'index senza cancellare i film
        document.getElementById('backBtn').addEventListener('click', function() {
            window.location.href = "index.html";
        });

        // Recupera il nome dell'algoritmo scelto
        const algoMap = {
            "KNN": "KNN",
            "MLOVIE": "MLOVIE"
        };
        const selectedAlgo = sessionStorage.getItem('selectedAlgorithm') || "KNN";
        const algoName = algoMap[selectedAlgo] || selectedAlgo;

        // Aggiorna l'intestazione
        const h2 = document.querySelector("#resultsBox h2");
        h2.textContent = `These are the results with ${algoName}:`;

        function tmdbType(type) {
            if (!type) return "movie";
            if (type.trim().toLowerCase() === "tv show") return "tv";
            return "movie";
        }

        function selectMovie(index) {
            if (movieDivs.length === 0) return;
            movieDivs.forEach(div => div.classList.remove("selected"));
            if (index < 0) index = 0;
            if (index >= movieDivs.length) index = movieDivs.length - 1;
            selectedIndex = index;
            const div = movieDivs[selectedIndex];
            div.classList.add("selected");
            popupLocked = true;
            lockedMovieDiv = div;
            const img = div.querySelector("img");
            const span = div.querySelector("span");
            const title = span.textContent;
            // Trova l'indice del titolo in movies
            const idx = movies.indexOf(title);
            const details = detailsArr[idx] || {};
            const type = details.type || "movie";
            let description = div.dataset.description || "";
            showPopup(img.src, title, description, div, details);
            if (!description) {
                getDescription(title, type).then(desc => {
                    div.dataset.description = desc;
                    if (lockedMovieDiv === div) showPopup(img.src, title, desc, div, details);
                });
            }
            div.scrollIntoView({ behavior: "smooth", block: "center" });
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