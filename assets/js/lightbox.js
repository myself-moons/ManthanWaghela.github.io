document.addEventListener('DOMContentLoaded', function() {
    // Create lightbox elements
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    const closeBtn = document.createElement('span');
    closeBtn.className = 'lightbox-close';
    closeBtn.innerHTML = '×';
    lightbox.appendChild(closeBtn);
    document.body.appendChild(lightbox);

    // Handle lightbox image clicks
    document.querySelectorAll('.lightbox-image').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const img = document.createElement('img');
            img.src = this.href;
            
            // Clear previous image
            while (lightbox.children.length > 1) {
                lightbox.removeChild(lightbox.lastChild);
            }
            
            lightbox.appendChild(img);
            lightbox.style.display = 'block';
            
            let isZoomed = false;
            let isDragging = false;
            let startX, startY, translateX = 0, translateY = 0;
            
            // Toggle zoom on image click
            img.addEventListener('click', function(e) {
                if (!isDragging) {
                    isZoomed = !isZoomed;
                    lightbox.classList.toggle('zoomed');
                    if (!isZoomed) {
                        img.style.transform = 'translate(-50%, -50%)';
                        translateX = 0;
                        translateY = 0;
                    }
                }
            });
            
            // Handle image dragging when zoomed
            img.addEventListener('mousedown', function(e) {
                if (isZoomed) {
                    isDragging = false;
                    startX = e.clientX - translateX;
                    startY = e.clientY - translateY;
                    
                    function mouseMoveHandler(e) {
                        isDragging = true;
                        translateX = e.clientX - startX;
                        translateY = e.clientY - startY;
                        img.style.transform = `translate(calc(-50% + ${translateX}px), calc(-50% + ${translateY}px))`;
                    }
                    
                    function mouseUpHandler() {
                        document.removeEventListener('mousemove', mouseMoveHandler);
                        document.removeEventListener('mouseup', mouseUpHandler);
                        setTimeout(() => {
                            isDragging = false;
                        }, 100);
                    }
                    
                    document.addEventListener('mousemove', mouseMoveHandler);
                    document.addEventListener('mouseup', mouseUpHandler);
                }
            });
        });
    });

    // Close lightbox when clicking outside image or on close button
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox || e.target.className === 'lightbox-close') {
            lightbox.style.display = 'none';
            lightbox.classList.remove('zoomed');
        }
    });
});