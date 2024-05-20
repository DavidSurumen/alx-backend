import { createClient } from 'redis';

const client = createClient();

client.on('error', (err) => console.log('Redis client not connected to the server:', err));
client.on('connect', () => console.log('Redis client connected to the server'));

client.subscribe('holberton school channel', (err, _count) => {
  if (err) console.log('Error subsribing to holberton school channel:', err);
});

client.on('message', (_channel, message) => {
  console.log(`${message}`);
  if (message === 'KILL_SERVER') {
    client.unsubscribe('holberton school channel', (err, _count) => {
      if (err) console.error('Unsubscription error:', err);
    });
    client.quit();
  }
});
