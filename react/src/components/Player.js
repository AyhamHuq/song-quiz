import React, { useEffect } from 'react';

async function fetchToken() {
    const response = await fetch('/token');
    const data = await response.json();
    return data.access_token;
}

const Player = () => {
    useEffect(() => {
        const script = document.createElement('script');
        script.src = 'https://sdk.scdn.co/spotify-player.js';
        script.async = true;
        script.onload = () => {
            window.onSpotifyWebPlaybackSDKReady = async () => {
                const token = await fetchToken();

                const player = new window.Spotify.Player({
                    name: 'Web Playback SDK',
                    getOAuthToken: cb => { cb(token); },
                    volume: 0.5
                });

                // Add Spotify player event listeners and connect the player
                player.addListener('ready', ({ device_id }) => {
                    console.log('Ready with Device ID', device_id);
                });

                player.addListener('not_ready', ({ device_id }) => {
                    console.log('Device ID has gone offline', device_id);
                });

                player.addListener('initialization_error', ({ message }) => {
                    console.error('Failed to initialize', message);
                });

                player.addListener('authentication_error', ({ message }) => {
                    console.error('Failed to authenticate', message);
                });

                player.addListener('account_error', ({ message }) => {
                    console.error('Failed to validate Spotify account', message);
                });

                player.addListener('playback_error', ({ message }) => {
                    console.error('Failed to perform playback', message);
                });

                await player.connect();
            };
        };
        document.body.appendChild(script);
    }, []);

    return (
        <div>
            <h1>Spotify Web Playback SDK</h1>
        </div>
    );
};

export default Player;
