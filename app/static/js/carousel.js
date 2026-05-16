document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.querySelector('.carousel-wrapper');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const nextBtn = document.querySelector('.carousel-btn.next');
    const slides = wrapper.querySelectorAll('.carousel-slide');
    const totalSlides = slides.length;
    let index = 0;
    const intervalTime = 5000; // 5 segundos para o ciclo automático

    const updateScroll = () => {
        const targetSlide = slides[index];
        if (!targetSlide) return;
        wrapper.scrollTo({
            left: targetSlide.offsetLeft - 10,
            behavior: 'smooth'
        });
    };

    const nextSlide = () => {
        index = (index + 1) % totalSlides;
        updateScroll();
    };

    const prevSlide = () => {
        index = (index - 1 + totalSlides) % totalSlides;
        updateScroll();
    };

    // Reinicia o temporizador quando o usuário interage manualmente
    const resetInterval = () => {
        clearInterval(slideInterval);
        slideInterval = setInterval(nextSlide, intervalTime);
    };

    let slideInterval = setInterval(nextSlide, intervalTime);

    nextBtn.addEventListener('click', () => { nextSlide(); resetInterval(); });
    prevBtn.addEventListener('click', () => { prevSlide(); resetInterval(); });

    // Pausa ao passar o mouse
    wrapper.addEventListener('mouseenter', () => clearInterval(slideInterval));
    wrapper.addEventListener('mouseleave', () => slideInterval = setInterval(nextSlide, intervalTime));

    // Ajusta o scroll caso a janela seja redimensionada
    window.addEventListener('resize', updateScroll);
});