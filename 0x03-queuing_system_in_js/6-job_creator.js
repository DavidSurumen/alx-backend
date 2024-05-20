import kue from 'kue';

const job_obj = {
  phoneNumber: '01234556',
  message: 'message string',
}

const push_notification_code = kue.createQueue();

const job = push_notification_code.create('notification', job_obj)
  .save((err) => {
  if (!err) console.log('Notification job created:', job.id);
  });

job.on('complete', () => {
  console.log('Notification job completed');
}).on('failed', () => {
  console.log('Notification job failed');
});
