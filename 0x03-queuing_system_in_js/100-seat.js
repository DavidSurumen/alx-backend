import { createClient } from 'redis';
import { createQueue } from 'kue';
import { promisify } from 'util';
import express from 'express';


let reservationEnabled = true;
const client = createClient();
const QUEUE = createQueue();

const app = express();
app.listen(1245);

client.on('error', (err) => console.error('Redis client not connected to server:', err));
client.set('available_seats', 50); // set initial number of seats when app launches

function reserveSeat(number) {
  client.set('available_seats', number);
}

const getAsync = promisify(client.get).bind(client);

async function getCurrentAvailableSeats() {
  return await getAsync('available_seats');
}

app.get('/available_seats', async (_req, res) => {
  const avail_sts = await getCurrentAvailableSeats();
  res.json({ "numberOfAvailableSeats": avail_sts });
});

app.get('/reserve_seat', (_req, res) => {
  if (!reservationEnabled) {
    res.json({ "status": "Reservation are blocked" });
    return;
  }

  const job = QUEUE.create("reserve_seat", "seat reservation")
  .save((err) => {
    if (err)
      res.json({ "status": "Reservation failed" });
    else
      res.json({ "status": "Reservation in process" });
  });

  job
  .on("complete", () => console.log(`Seat reservation job ${job.id} completed`))
  .on("failed", (err) => console.log(`Seat reservation job ${job.id} failed: ${err}`));
});

app.get('/process', (_req, res) => {
  QUEUE.process("reserve_seat", async (job, done) => {
    // decrease the number of seats available
    const seats = await getCurrentAvailableSeats() - 1;
    if (seats >= 0)
      reserveSeat(seats);

    if (seats === 0) {
      reservationEnabled = false;
      done();
    }
    else if (seats > 0)
      done();
    else
      done(new Error('Not enough seats available'));
  });
  res.json({ "status": "Queue processing" });
});

if (client.connected) {
  client.quit();
}
