document.addEventListener('DOMContentLoaded', () => {
    // Add neon glow effect to cards on hover
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.boxShadow = '0 0 25px var(--neon-purple)';
            card.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.boxShadow = 'none';
            card.style.transform = 'translateY(0)';
        });
    });
    
    // Add loading animations
    const loadingElements = document.querySelectorAll('.loading-fade-in');
    loadingElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
            element.style.transition = 'all 0.5s ease';
        }, 100);
    });
});
