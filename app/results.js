// Recupera i film dalla sessionStorage
        const movies = JSON.parse(sessionStorage.getItem('suggestedMovies') || "[]");
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

        function showPopup(imgSrc, title, description, anchorDiv) {
            // Imposta il contenuto
            popup.innerHTML = `
                <img src="${imgSrc}" alt="${title}" class="popup-cover" />
                <div class="popup-info">
                    <div class="popup-title">${title}</div>
                    <div class="popup-desc">${description}</div>
                </div>
            `;
            popup.style.position = "fixed";
            popup.style.display = "flex";
            popup.style.visibility = "hidden";
            // RIMUOVI eventuale animazione precedente
            popup.style.animation = "none";

            // Calcola la posizione
            const filmRect = anchorDiv.getBoundingClientRect();
            const popupWidth = popup.offsetWidth;
            const left = window.innerWidth / 2 + 80 - popupWidth / 2;
            popup.style.left = `${left}px`;
            popup.style.top = `${filmRect.top + filmRect.height / 2}px`;
            popup.style.transform = "translateY(-50%)";

            // Ora rendi visibile il popup e applica l’animazione
            popup.style.visibility = "visible";
            // Forza il reflow per riapplicare l’animazione
            void popup.offsetWidth;
            popup.style.animation = "fadeIn 0.18s";
        }

        function hidePopup() {
            if (!popupLocked) {
                popup.style.display = "none";
                lockedMovieDiv = null;
            }
        }

        movies.forEach(title => {
            const div = document.createElement("div");
            div.className = "suggestion-movie";
            div.style.display = "flex";
            div.style.alignItems = "center";
            div.style.justifyContent = "space-between";
            div.style.gap = "0.7rem";
            div.style.marginBottom = "2rem";

            const img = document.createElement("img");
            img.src = "placeholder.png";
            img.alt = title;
            img.className = "results-cover";

            const span = document.createElement("span");
            span.textContent = title;
            span.style.flex = "1";
            span.style.marginLeft = "0.5rem";

            const description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque euismod, nisi vel consectetur.";

            // Hover: mostra solo se non bloccato o se è il film bloccato
            div.addEventListener("mouseenter", () => {
                if (!popupLocked || lockedMovieDiv === div) {
                    showPopup(img.src, title, description, div);
                }
            });
            div.addEventListener("mouseleave", () => {
                if (!popupLocked || lockedMovieDiv !== div) {
                    hidePopup();
                }
            });

            // Click: blocca/sblocca il popup
            div.addEventListener("click", () => {
                if (popupLocked && lockedMovieDiv === div) {
                    popupLocked = false;
                    hidePopup();
                } else {
                    popupLocked = true;
                    lockedMovieDiv = div;
                    showPopup(img.src, title, description, div);
                }
            });

            div.appendChild(img);
            div.appendChild(span);
            resultsBox.appendChild(div);
        });

        // Se clicchi fuori dal popup e da ogni film, sblocca e nascondi il popup
        document.addEventListener("click", function(e) {
            if (
                popupLocked &&
                !popup.contains(e.target) &&
                !e.target.classList.contains("suggestion-movie") &&
                !e.target.classList.contains("results-cover")
            ) {
                popupLocked = false;
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
        }
        toggle.addEventListener("click", () => {
            document.body.classList.toggle("dark");
            const isDark = document.body.classList.contains("dark");
            icon.textContent = isDark ? "🌙" : "☀️";
            localStorage.setItem("theme", isDark ? "dark" : "light");
        });
        applyTheme();
        document.documentElement.classList.remove("dark-preload");

        // Pulsante "Back" per tornare all'index senza cancellare i film
        document.getElementById('backBtn').addEventListener('click', function() {
            window.location.href = "index.html";
        });

        // Recupera il nome dell'algoritmo scelto
        const algoMap = {
            "algo1": "Algorithm 1",
            "algo2": "Algorithm 2"
        };
        const selectedAlgo = sessionStorage.getItem('selectedAlgorithm') || "algo1";
        const algoName = algoMap[selectedAlgo] || selectedAlgo;

        // Aggiorna l'intestazione
        const h2 = document.querySelector("#resultsBox h2");
        h2.textContent = `These are the results with ${algoName}:`;