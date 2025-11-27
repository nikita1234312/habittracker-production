function openModal() {
    const modal = document.getElementById('modalOverlay');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    const coverElement = document.querySelector('.cover-container');
    originalCoverStyle = coverElement.style.backgroundImage;
    const avatarElement = document.querySelector('.modal-profile-avatar');
    originalAvatarHTML = avatarElement.innerHTML;
    }

    function closeModal() {
        const modal = document.getElementById('modalOverlay');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';

        const avatarElement = document.querySelector('.modal-profile-avatar');
        avatarElement.innerHTML = originalAvatarHTML;
        const coverElement = document.querySelector('.cover-container');
        coverElement.style.backgroundImage = originalCoverStyle;

        document.getElementById('avaInput').value = '';
        document.getElementById('coverInput').value = '';
    }

    function handleOverlayClick(event) {
        const modalOverlay = document.getElementById('modalOverlay');
        if (event.target === modalOverlay) {
            closeModal();
        }
    }


    function showCover() {
        const fileInput = document.getElementById('coverInput');
        const file = fileInput.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('modal-cover').style.backgroundImage = 'url(' + e.target.result + ')';
            }
            reader.readAsDataURL(file);
        }
    }

    function showAva() {
        const fileInput = document.getElementById('avaInput');
        const file = fileInput.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const avatarElement = document.querySelector('.modal-profile-avatar')
                avatarElement.innerHTML = `<img src="${e.target.result}" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;">`;
            }
            reader.readAsDataURL(file)
        }
    }


    function getCookie(name) {
        let cookieValue = null;
        
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    let originalCoverStyle = '';
    let originalAvatarHTML = '';


    window.addEventListener('load', function() {
        const modalOverlay = document.getElementById('modalOverlay');
        const form = document.querySelector('form');
        
        if (modalOverlay) {
            modalOverlay.addEventListener('click', handleOverlayClick);
        }
        
        if (form) {
            form.addEventListener('submit', function(e) {
                return true;
            });
        }
    });