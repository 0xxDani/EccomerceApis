// FUNCIÓN PARA MOVER LAS FOTOS DEL CONTENEDOR PRINCIPAL
console.log('-Archivo diapositivas funcionando, si estas leyendo esto Inhala...Exhala...Ahhh....Continuemos');

document.addEventListener("DOMContentLoaded", function () {
    // Lista de URLs permitidas
    const allowedURLs = ["/contact/", "/about/"]; // Agrega más URLs según sea necesario

    // Verifica si la URL actual está permitida
    if (allowedURLs.includes(window.location.pathname)) {
        let currentIndex = 0;
        const slides = document.querySelectorAll(".diapositiva-2");
        const totalSlides = slides.length;

        function showSlide(index) {
            const percentage = -(index * (100 / totalSlides));
            document.querySelector(".diapositivas-2").style.transform = `translateX(${percentage}%)`;
        }

        function nextSlide() {
            currentIndex = (currentIndex + 1) % totalSlides;
            showSlide(currentIndex);
        }

        setInterval(nextSlide, 4000); // Cambia la diapositiva cada 4 segundos
    } else {
        console.log('-Archivo diapositivas.js parado en esta página');
    }
});
