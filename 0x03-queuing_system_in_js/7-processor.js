import { createQueue } from 'kue';

const queue = createQueue({ maxConcurrency: 2 });

const blacklist = ['4153518780', '4153518781'];

function sendNotification(phoneNumber, message, job, done) {
  job.progress(0, 100);
  if (blacklist.includes(phoneNumber)) {
    // fail the job and return an Error
    done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  } else {
    job.progress(50, 100);
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
    done();
  }
}

queue.process('push_notification_code_2', 2, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
