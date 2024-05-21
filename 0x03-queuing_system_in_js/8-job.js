import { createQueue } from 'kue';


const queue = createQueue();

/**
 * Creates jobs from the given array of objects
 *
 * @param {Array} jobs An Array of objects
 * @param {kue.Queue} queue The Kue queue instance to create jobs from
 */
export default function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }
  for (const item of jobs) {
    const job = queue.create('push_notification_code_3', item);

    job
    .on('enqueue', () => console.log(`Notification job created: ${job.id}`))
    .on('complete', () => console.log(`Notification job ${job.id} completed`))
    .on('failed', (err) => console.log(`Notification job ${job.id} failed: ${err}`))
    .on('progress', (progress) => console.log(`Notification job ${job.id} ${progress}% complete`));

    job.save();
  }
}
