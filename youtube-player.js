const iframe = document.getElementById('youtube-iframe');
let buttons = document.querySelectorAll('#button-container button');

async function loadPlaylist() {
    try {
        const response = await fetch('input.json');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const playlist = await response.json();

        function changeChannel(channelId) {
            iframe.src = `https://www.youtube.com/embed/live_stream?channel=${channelId}&autoplay=1`;
            localStorage.setItem('lastChannel', channelId);
            updateActiveButton(channelId);
        }

        function updateActiveButton(channelId) {
            buttons.forEach(btn => {
                btn.classList.toggle('active', btn.dataset.channel === channelId);
            });
        }

        const lastChannel = localStorage.getItem('lastChannel') || playlist[1].channel_id;
        changeChannel(lastChannel);

        const buttonContainer = document.getElementById('button-container');
        playlist.forEach(channel => {
            const button = document.createElement('button');
            button.dataset.channel = channel["channel-id"];
            button.textContent = channel["name"];
            button.addEventListener('click', () => changeChannel(channel["channel-id"]));
            buttonContainer.appendChild(button);
        });
        buttons = document.querySelectorAll('#button-container button');
    } catch (error) {
        console.error('Error loading playlist:', error);
    }
}

loadPlaylist();
