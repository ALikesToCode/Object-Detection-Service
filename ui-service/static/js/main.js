document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const dropZone = document.getElementById('drop-zone');
    const imageInput = document.getElementById('image-input');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('preview-image');
    const changeImageBtn = document.getElementById('change-image');
    const detectButton = document.getElementById('detect-button');
    const loadingIndicator = document.getElementById('loading');
    const resultsSection = document.getElementById('results');

    let isProcessing = false;

    const modal = document.getElementById('fullscreen-modal');
    const modalImage = document.getElementById('modal-image');
    const closeBtn = modal.querySelector('.close-btn');
    const downloadBtn = modal.querySelector('.download-btn');
    
    function openModal(imageSrc) {
        modalImage.src = imageSrc;
        modal.style.display = 'flex';
        setTimeout(() => modal.classList.add('active'), 10);
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.classList.remove('active');
        setTimeout(() => {
            modal.style.display = 'none';
            modalImage.src = '';
        }, 300);
        document.body.style.overflow = '';
    }

    function downloadImage() {
        const link = document.createElement('a');
        link.href = modalImage.src;
        link.download = 'detected-image.jpg';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    document.querySelectorAll('.fullscreen-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const imageType = this.dataset.image;
            const image = imageType === 'preview' ? 
                document.getElementById('preview-image') : 
                document.getElementById('result-image');
            openModal(image.src);
        });
    });

    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function(e) {
        if (e.target === modal) closeModal();
    });

    downloadBtn.addEventListener('click', downloadImage);

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            closeModal();
        }
    });

    function showPreview(file) {
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                dropZone.style.display = 'none';
                previewContainer.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    }

    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            showPreview(file);
            resultsSection.style.display = 'none';
        } else if (file) {
            alert('Please select an image file');
            imageInput.value = '';
        }
    });

    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            imageInput.files = e.dataTransfer.files;
            showPreview(file);
            resultsSection.style.display = 'none';
        } else {
            alert('Please drop an image file');
        }
    });

    changeImageBtn.addEventListener('click', function() {
        previewContainer.style.display = 'none';
        dropZone.style.display = 'block';
        imageInput.value = '';
        previewImage.src = '';
        resultsSection.style.display = 'none';
        isProcessing = false;
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (isProcessing) return;
        
        const file = imageInput.files[0];
        if (!file) {
            alert('Please select an image first');
            return;
        }

        try {
            isProcessing = true;
            detectButton.disabled = true;
            loadingIndicator.style.display = 'flex';
            resultsSection.style.display = 'none';

            const formData = new FormData();
            formData.append('file', file, file.name);

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (!response.ok || data.error) {
                throw new Error(data.error || 'Failed to process image');
            }

            const resultImage = new Image();
            
            resultImage.onload = function() {
                document.getElementById('result-image').src = resultImage.src;
                
                const formattedJson = JSON.stringify(data.result, null, 2);
                document.getElementById('json-results').textContent = formattedJson;
                
                loadingIndicator.style.display = 'none';
                resultsSection.style.display = 'block';
                
                detectButton.disabled = false;
                isProcessing = false;
            };

            resultImage.onerror = function() {
                console.error('Failed to load image:', data.detected_image);
                loadingIndicator.style.display = 'none';
                detectButton.disabled = false;
                isProcessing = false;
                alert('Failed to load the detected image');
            };

            const timestamp = new Date().getTime();
            resultImage.src = `${data.detected_image}?t=${timestamp}`;

        } catch (error) {
            console.error('Error:', error);
            alert('Error: ' + error.message);
            loadingIndicator.style.display = 'none';
            detectButton.disabled = false;
            isProcessing = false;
            resultsSection.style.display = 'none';
        }
    });
}); 