import { Queue } from "bullmq";
import { redis } from "./redis";

export const reminderQueue = new Queue("appointment-reminders", {
  connection: redis,
  defaultJobOptions: {
    removeOnComplete: 100,
    removeOnFail: 50,
  },
});

export async function scheduleReminder(appointmentId: string, sendAt: Date) {
  const delay = sendAt.getTime() - Date.now();
  if (delay < 0) return null;

  const job = await reminderQueue.add(
    "send-reminder",
    { appointmentId },
    { delay, jobId: `reminder-${appointmentId}` }
  );
  return job.id;
}

export async function cancelReminder(appointmentId: string) {
  const job = await reminderQueue.getJob(`reminder-${appointmentId}`);
  if (job) await job.remove();
}
