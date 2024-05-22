import createPushNotificationsJobs from './8-job.js';
import { createQueue } from 'kue';
import assert from 'assert';
import sinon from 'sinon';


describe("#createPushNotificationsJobs", () => {
  const QUEUE = createQueue();
  const consoleLogSpy = sinon.spy(console, "log");

  before(() => {
    QUEUE.testMode.enter(true);
  });

  beforeEach(() => {
    //consoleLogStub = sinon.spy(console, "log");
    //consoleErrorStub = sinon.stub(console, "error");
  });

  afterEach(() => {
    consoleLogSpy.resetHistory();
    //consoleErrorStub.restore();
  });

  after(() => {
    QUEUE.testMode.clear();
    QUEUE.testMode.exit();
  });

  it('throws an error object when jobs is not an array', (done) => {
    const callerFunc = () => {
      createPushNotificationsJobs({}, QUEUE);
    }
    assert.throws(callerFunc, Error, 'Jobs is not an array');
    done();
  });

  it('creates two new jobs to the queue', (done) => {
    const jobData = [
      {
        title: "Test Job",
        details: "Some data"
      },
      {
        phoneNumber: '2324383434',
        message: 'Use the code 9034 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobData, QUEUE);

    // verify the job is created in test mode
    assert.strictEqual(QUEUE.testMode.jobs.length, 2);
    assert.strictEqual(QUEUE.testMode.jobs[0].type, "push_notification_code_3");

    // verify console output on successful job creation
    QUEUE.process('push_notification_code_3', () => {
      assert(consoleLogSpy.calledWith(`Notification job created: ${QUEUE.testMode.jobs[0].id}`));
      done();
    });
  });

  it('registers the complete event handler', (done) => {
    createPushNotificationsJobs([{title: 'test993932', message: 'test complete'}], QUEUE);
    QUEUE.testMode.jobs[0].emit('complete');
    assert(consoleLogSpy.calledWith(`Notification job ${QUEUE.testMode.jobs[0].id} completed`));
    done();
  });

  it('registers the failed event handler', (done) => {
    createPushNotificationsJobs([{title: 'test'}], QUEUE);
    QUEUE.testMode.jobs[0].emit('failed', new Error('Job failed'));
    assert(consoleLogSpy.calledWithMatch(`Notification job ${QUEUE.testMode.jobs[0].id} failed`));
    done();
  });

  it('registers the progress event handler', (done) => {
    createPushNotificationsJobs([{title: 'test'}], QUEUE);
    QUEUE.testMode.jobs[0].emit('progress', 60);
    assert(consoleLogSpy.calledWith(`Notification job ${QUEUE.testMode.jobs[0].id} 60% complete`));
    done();
  });
});
