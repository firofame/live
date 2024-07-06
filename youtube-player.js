const iframe = document.getElementById('youtube-iframe');
const buttons = document.querySelectorAll('#button-container button');

function changeChannel(channelId) {
    console.log(`Changing channel to ${channelId}`);
    iframe.src = `https://www.youtube.com/embed/live_stream?channel=${channelId}&autoplay=1`;
    localStorage.setItem('lastChannel', channelId);
    updateActiveButton(channelId);
}

function updateActiveButton(channelId) {
    buttons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.channel === channelId);
    });
}

// Load last viewed channel or default to the first channel
const lastChannel = localStorage.getItem('lastChannel') || buttons[0].dataset.channel;
changeChannel(lastChannel);

fetch('playlist.json')
    .then(response => response.json())
    .then(data => {
        const buttonContainer = document.getElementById('button-container');
        data.forEach(channel => {
            const button = document.createElement('button');
            button.dataset.channel = channel.channel_id;
            button.textContent = channel.channel_name;
            button.addEventListener('click', () => changeChannel(channel.channel_id));
            buttonContainer.appendChild(button);
        });
    });
