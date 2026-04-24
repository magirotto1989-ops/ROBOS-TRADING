import { Worker, Queue } from "bullmq";
import { Redis } from "ioredis";
import { prisma } from "@clinic/database";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

const EVOLUTION_URL = process.env.EVOLUTION_API_URL!;
const EVOLUTION_KEY = process.env.EVOLUTION_API_KEY!;
const INSTANCE = process.env.EVOLUTION_INSTANCE!;

const connection = new Redis(process.env.REDIS_URL!, {
  maxRetriesPerRequest: null,
});

async function sendWhatsApp(phone: string, text: string) {
  const res = await fetch(`${EVOLUTION_URL}/message/sendText/${INSTANCE}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      apikey: EVOLUTION_KEY,
    },
    body: JSON.stringify({ number: phone, text }),
  });
  if (!res.ok) {
    throw new Error(`Evolution API error: ${res.status} ${await res.text()}`);
  }
}

const worker = new Worker(
  "appointment-reminders",
  async (job) => {
    const { appointmentId } = job.data as { appointmentId: string };

    const appointment = await prisma.appointment.findUnique({
      where: { id: appointmentId },
      include: {
        patient: true,
        professional: { select: { name: true, specialty: true } },
        clinic: { select: { name: true } },
      },
    });

    if (!appointment) {
      console.log(`[Worker] Appointment ${appointmentId} not found — skipping`);
      return;
    }

    if (appointment.status === "CANCELLED") {
      console.log(`[Worker] Appointment ${appointmentId} is cancelled — skipping`);
      return;
    }

    const dateLabel = format(appointment.dateTime, "EEEE, dd 'de' MMMM 'às' HH:mm", { locale: ptBR });

    const message =
      `Olá, *${appointment.patient.name}*! 👋\n\n` +
      `Este é um lembrete da sua consulta:\n\n` +
      `👨‍⚕️ *${appointment.professional.name}*\n` +
      `🏥 ${appointment.professional.specialty}\n` +
      `📅 ${dateLabel}\n\n` +
      `Por favor, confirme sua presença respondendo *SIM* ou cancele respondendo *CANCELAR*.\n\n` +
      `_${appointment.clinic.name}_`;

    await sendWhatsApp(appointment.patient.phone, message);

    await prisma.appointment.update({
      where: { id: appointmentId },
      data: { reminderSent: true },
    });

    console.log(`[Worker] Reminder sent for appointment ${appointmentId} → ${appointment.patient.phone}`);
  },
  {
    connection,
    concurrency: 5,
    removeOnComplete: { count: 100 },
    removeOnFail: { count: 50 },
  }
);

worker.on("completed", (job) => {
  console.log(`[Worker] Job ${job.id} completed`);
});

worker.on("failed", (job, err) => {
  console.error(`[Worker] Job ${job?.id} failed:`, err.message);
});

worker.on("error", (err) => {
  console.error("[Worker] Error:", err);
});

console.log("[Worker] Reminder worker started. Waiting for jobs...");

// Auto-confirm appointments when patient replies SIM
// This logic lives in the chatbot; the worker only sends reminders

process.on("SIGTERM", async () => {
  await worker.close();
  await prisma.$disconnect();
  process.exit(0);
});
