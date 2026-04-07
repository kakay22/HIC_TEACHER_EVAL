document.addEventListener('DOMContentLoaded', () => {

    const toastElList = document.querySelectorAll('.toast');

    toastElList.forEach(toastEl => {

        const toast = new bootstrap.Toast(toastEl, {
            delay: 2000,
            autohide: true
        });

        toast.show();

        // Swipe to dismiss
let startX = 0;
let currentX = 0;
let isDragging = false;

toastEl.addEventListener('touchstart', e => {
    startX = e.touches[0].clientX;
    isDragging = true;
    toastEl.style.transition = '';
});

toastEl.addEventListener('touchmove', e => {
    if (!isDragging) return;

    currentX = e.touches[0].clientX;
    const deltaX = currentX - startX;

    toastEl.style.transform = `translateX(${deltaX}px)`;
    toastEl.style.opacity = 1 - Math.abs(deltaX) / 200;
});

toastEl.addEventListener('touchend', () => {

    isDragging = false;
    const deltaX = currentX - startX;

    if (Math.abs(deltaX) > 120) {

        // Animate toast halfway outside the screen
        toastEl.style.transition = 'transform 0.35s ease, opacity 0.35s ease';

        const direction = deltaX > 0 ? 1 : -1;
        toastEl.style.transform = `translateX(${direction * window.innerWidth * 0.6}px)`;
        toastEl.style.opacity = 0;

        // Hide after animation
        setTimeout(() => {
            toast.hide();
        }, 350);

    } else {

        // Return to original position
        toastEl.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
        toastEl.style.transform = 'translateX(0)';
        toastEl.style.opacity = 1;

    }

});

    });

});