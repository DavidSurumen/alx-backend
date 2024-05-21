import kue from 'kue';

const job_obj = {
  phoneNumber: '0123456789',
  message: 'job created.',
}

const queue = kue.createQueue();

const job = queue.create('push_notification_code', job_obj)
  .save((err) => {
  if (!err) console.log('Notification job created:', job.id);
  });

job.on('complete', () => {
  console.log('Notification job completed');
}).on('failed', () => {
  console.log('Notification job failed');
});
