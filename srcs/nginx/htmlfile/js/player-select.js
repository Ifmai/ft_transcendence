async function how_to_play(){
    const arrowUp = document.querySelector('.idx-arrow-up');
    const arrowDown = document.querySelector('.idx-arrow-down');
    const spaceBar = document.querySelector('.idx-space-bar');
    if (!arrowUp || !arrowDown || !spaceBar) {
        console.error('One or more key elements not found');
        return;
    }
    const highlightKey = (element) => {
        if (element) {
            element.style.backgroundColor = 'var(--neon-orange)';
        }
    };

    const unhighlightKey = (element) => {
        if (element) {
            element.style.backgroundColor = 'var(--neon-blue)';
        }
    };

    // Mouse event listeners
    [arrowUp, arrowDown, spaceBar].forEach((element) => {
        if (element) {
            element.addEventListener('mousedown', () => highlightKey(element));
            element.addEventListener('mouseup', () => unhighlightKey(element));
            element.addEventListener('mouseleave', () => unhighlightKey(element));
        }
    });

    // Keyboard event listeners
    document.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowUp') {
			event.preventDefault(); // Varsayılan davranışı engelle
            highlightKey(arrowUp);
        } else if (event.key === 'ArrowDown') {
			event.preventDefault(); // Varsayılan davranışı engelle
            highlightKey(arrowDown);
        } else if (event.key === ' ') {
			event.preventDefault(); // Varsayılan davranışı engelle
            highlightKey(spaceBar);
        }
    });

    document.addEventListener('keyup', (event) => {
        if (event.key === 'ArrowUp') {
            unhighlightKey(arrowUp);
        } else if (event.key === 'ArrowDown') {
            unhighlightKey(arrowDown);
        } else if (event.key === ' ') {
            unhighlightKey(spaceBar);
        }
    });
}
