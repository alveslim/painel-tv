document.addEventListener("DOMContentLoaded", function () {
    const slides = document.querySelectorAll(".slide-item");
    const btnNext = document.getElementById("btn-next");
    const progressBar = document.querySelector(".progress-bar-fill");
    const tvCard = document.querySelector(".tv-card");

    // Cria a caixinha de aviso "Pausado" dinamicamente (não precisa mexer no HTML)
    let pauseIndicator = document.getElementById("pause-indicator");
    if (!pauseIndicator) {
        pauseIndicator = document.createElement("div");
        pauseIndicator.id = "pause-indicator";
        pauseIndicator.className = "pause-indicator";
        pauseIndicator.innerHTML = "⏸ PAUSADO (Tire o mouse da tela para retomar)";
        document.body.appendChild(pauseIndicator);
    }

    let currentSlide = 0;
    let slideInterval;
    let isPaused = false;
    const TIME_PER_SLIDE = 30000; // 30 segundos

    // Função que avança a tela
    function nextSlide() {
        slides[currentSlide].classList.remove("active");
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.add("active");
    }

    // Identifica se é celular
    function isMobile() {
        return window.innerWidth <= 850;
    }

    // Reseta a barrinha azul de baixo
    function resetAnimation() {
        if (progressBar) {
            progressBar.style.animation = "none";
            void progressBar.offsetWidth; // Truque para forçar o recomeço
            progressBar.style.animation = `progressLoop ${TIME_PER_SLIDE / 1000}s linear infinite`;
            progressBar.style.animationPlayState = "running";
        }
    }

    // Dá o Play na TV
    function startTimer() {
        clearInterval(slideInterval);

        // Se for celular ou estiver pausado, não roda o timer
        if (isMobile() || isPaused) {
            if (progressBar) progressBar.style.animation = "none";
            return;
        }

        slideInterval = setInterval(nextSlide, TIME_PER_SLIDE);
        resetAnimation();
        pauseIndicator.classList.remove("visible");
    }

    // Pausa a TV quando passa o mouse
    function pauseTimer() {
        if (isMobile()) return; // No celular isso não se aplica
        isPaused = true;
        clearInterval(slideInterval);
        if (progressBar) {
            progressBar.style.animationPlayState = "paused"; // Congela a barrinha
        }
        pauseIndicator.classList.add("visible"); // Mostra o aviso
    }

    // Retoma a TV quando tira o mouse
    function resumeTimer() {
        if (isMobile()) return;
        isPaused = false;
        startTimer();
    }

    // Botão de pular slide (Funciona no PC e no Celular)
    if (btnNext) {
        btnNext.addEventListener("click", function (e) {
            e.stopPropagation();
            nextSlide();
            if (!isMobile() && !isPaused) {
                startTimer(); // Recomeça a contar os 30s
            }
        });
    }

    // Eventos do Mouse na TV/PC
    if (tvCard) {
        tvCard.addEventListener("mouseenter", pauseTimer);
        tvCard.addEventListener("mouseleave", resumeTimer);
    }

    // Se a tela for redimensionada (Ex: virar o celular)
    window.addEventListener("resize", function () {
        if (isMobile()) {
            isPaused = false;
            pauseIndicator.classList.remove("visible");
        }
        startTimer();
    });

    // Inicia a aplicação
    startTimer();
});
