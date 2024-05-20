import { createClient } from 'redis';
import redis from 'redis';
import { promisify } from 'util';

const client = createClient();

client.on('error', err => console.error('Redis client not connected to the server:', err));

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const getAsync = promisify(client.get).bind(client);

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.log(value);
  } catch (err) {
    console.error('Error getting school:', err);
  }
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');

if (client.connected) {
  client.quit();
}
