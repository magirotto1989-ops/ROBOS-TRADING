import Anthropic from "@anthropic-ai/sdk";
import { prisma } from "./db";
import { sendTextMessage } from "./evolution";
import { scheduleReminder } from "./queue";
import { format, addHours, startOfDay, endOfDay, parseISO } from "date-fns";
import { ptBR } from "date-fns/locale";
import type {
  ConversationState,
  WhatsAppConversation,
  Patient,
} from "@clinic/database";

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

const CLINIC_ID = process.env.CLINIC_ID ?? "default";

// ──────────────────────────────────────────────
// INTENT DETECTION via Claude
// ──────────────────────────────────────────────

type Intent =
  | "SCHEDULE"
  | "CANCEL"
  | "WAITING_LIST"
  | "CONFIRM"
  | "STATUS"
  | "SUPPORT"
  | "GREETING"
  | "UNKNOWN";

async function detectIntent(message: string): Promise<Intent> {
  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 50,
    system: `Você é um classificador de intenções para um chatbot de consultório médico/odontológico.
Classifique a mensagem do paciente em UMA das categorias:
- SCHEDULE: quer agendar consulta
- CANCEL: quer cancelar consulta
- WAITING_LIST: quer entrar na fila de espera
- CONFIRM: confirmando algo (sim, confirmo, ok, pode ser)
- STATUS: quer saber status/informações de consulta existente
- SUPPORT: dúvidas, reclamações, outras perguntas
- GREETING: saudação sem intenção clara (oi, olá, bom dia)
- UNKNOWN: não identificado

Responda APENAS com a categoria, sem explicação.`,
    messages: [{ role: "user", content: message }],
  });

  const text = (response.content[0] as { text: string }).text.trim().toUpperCase();
  const valid: Intent[] = ["SCHEDULE", "CANCEL", "WAITING_LIST", "CONFIRM", "STATUS", "SUPPORT", "GREETING", "UNKNOWN"];
  return valid.includes(text as Intent) ? (text as Intent) : "UNKNOWN";
}

async function extractInfo(
  message: string,
  fields: string[]
): Promise<Record<string, string | null>> {
  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 200,
    system: `Extraia as seguintes informações da mensagem em JSON: ${fields.join(", ")}.
Se não encontrar um campo, retorne null para ele.
Retorne APENAS o JSON, sem explicação.
Para datas: converta para formato ISO (YYYY-MM-DD).
Para horários: converta para formato HH:MM.
Para telefone: apenas dígitos, com DDD.`,
    messages: [{ role: "user", content: message }],
  });

  try {
    const text = (response.content[0] as { text: string }).text.trim();
    const json = text.replace(/```json\n?|\n?```/g, "");
    return JSON.parse(json);
  } catch {
    return Object.fromEntries(fields.map((f) => [f, null]));
  }
}

// ──────────────────────────────────────────────
// MAIN HANDLER
// ──────────────────────────────────────────────

export async function handleWhatsAppMessage(phone: string, message: string) {
  const normalizedPhone = phone.replace(/\D/g, "");

  let conversation = await prisma.whatsAppConversation.findUnique({
    where: { phone: normalizedPhone },
    include: { patient: true },
  });

  if (!conversation) {
    conversation = await prisma.whatsAppConversation.create({
      data: { phone: normalizedPhone, state: "IDLE" },
      include: { patient: true },
    });
  }

  // Log incoming message
  await prisma.chatMessage.create({
    data: {
      conversationId: conversation.id,
      fromPatient: true,
      content: message,
    },
  });

  const reply = await processMessage(conversation, message, normalizedPhone);

  // Send reply and log it
  await sendTextMessage(normalizedPhone, reply);
  await prisma.chatMessage.create({
    data: {
      conversationId: conversation.id,
      fromPatient: false,
      content: reply,
    },
  });

  await prisma.whatsAppConversation.update({
    where: { id: conversation.id },
    data: { lastMessage: new Date() },
  });
}

async function processMessage(
  conv: WhatsAppConversation & { patient: Patient | null },
  message: string,
  phone: string
): Promise<string> {
  const ctx = (conv.context as Record<string, unknown>) ?? {};
  const state = conv.state;

  // ── Reset se digitar "menu" ou "cancelar" a qualquer momento
  if (/^(menu|início|inicio|voltar|restart)$/i.test(message.trim())) {
    await setState(conv.id, "MENU", {});
    return buildMenuMessage(conv.patient?.name);
  }

  switch (state) {
    case "IDLE":
    case "GREETING":
      return handleIdle(conv, message, phone, ctx);

    case "IDENTIFYING":
      return handleIdentifying(conv, message, phone, ctx);

    case "MENU":
      return handleMenu(conv, message, phone, ctx);

    case "SCHEDULING_SPECIALTY":
      return handleSchedulingSpecialty(conv, message, phone, ctx);

    case "SCHEDULING_PROFESSIONAL":
      return handleSchedulingProfessional(conv, message, phone, ctx);

    case "SCHEDULING_DATE":
      return handleSchedulingDate(conv, message, phone, ctx);

    case "SCHEDULING_TIME":
      return handleSchedulingTime(conv, message, phone, ctx);

    case "SCHEDULING_CONFIRM":
      return handleSchedulingConfirm(conv, message, phone, ctx);

    case "CANCELLING":
      return handleCancelling(conv, message, phone, ctx);

    case "CANCELLING_CONFIRM":
      return handleCancellingConfirm(conv, message, phone, ctx);

    case "WAITING_LIST":
      return handleWaitingList(conv, message, phone, ctx);

    default:
      await setState(conv.id, "MENU", {});
      return buildMenuMessage(conv.patient?.name);
  }
}

// ──────────────────────────────────────────────
// STATE HANDLERS
// ──────────────────────────────────────────────

async function handleIdle(
  conv: WhatsAppConversation & { patient: Patient | null },
  message: string,
  phone: string,
  _ctx: Record<string, unknown>
): Promise<string> {
  if (!conv.patient) {
    await setState(conv.id, "IDENTIFYING", {});
    return `Olá! Bem-vindo(a) à nossa clínica! 😊\n\nSou o assistente virtual e estou aqui para te ajudar.\n\nPara começar, pode me dizer seu *nome completo*?`;
  }

  await setState(conv.id, "MENU", {});
  return buildMenuMessage(conv.patient.name);
}

async function handleIdentifying(
  conv: WhatsAppConversation & { patient: Patient | null },
  message: string,
  phone: string,
  ctx: Record<string, unknown>
): Promise<string> {
  if (!ctx.name) {
    const extracted = await extractInfo(message, ["name"]);
    const name = extracted.name ?? message.trim();
    await setState(conv.id, "IDENTIFYING", { name });
    return `Prazer, *${name}*! 😊\n\nPode me informar seu *CPF* (apenas números) para localizar seu cadastro?\n\n_Se preferir, envie "pular" para continuar sem CPF._`;
  }

  const name = ctx.name as string;
  let cpf: string | null = null;

  if (!/pular/i.test(message)) {
    const digits = message.replace(/\D/g, "");
    if (digits.length === 11) cpf = digits;
  }

  // Procura paciente existente pelo CPF ou cria novo
  let patient = cpf
    ? await prisma.patient.findFirst({ where: { cpf, clinicId: CLINIC_ID } })
    : null;

  if (!patient) {
    patient = await prisma.patient.upsert({
      where: { clinicId_phone: { clinicId: CLINIC_ID, phone } },
      update: { name, cpf: cpf ?? undefined },
      create: { clinicId: CLINIC_ID, name, phone, cpf },
    });
  }

  await prisma.whatsAppConversation.update({
    where: { id: conv.id },
    data: { patientId: patient.id },
  });

  await setState(conv.id, "MENU", {});
  return buildMenuMessage(patient.name);
}

async function handleMenu(
  conv: WhatsAppConversation & { patient: Patient | null },
  message: string,
  phone: string,
  _ctx: Record<string, unknown>
): Promise<string> {
  const intent = await detectIntent(message);
  const num = message.trim();

  if (num === "1" || intent === "SCHEDULE") {
    await setState(conv.id, "SCHEDULING_SPECIALTY", {});
    const specialties = await getSpecialties();
    return `Ótimo! Vamos agendar sua consulta. 📅\n\nQual *especialidade* você precisa?\n\n${specialties.map((s, i) => `*${i + 1}.* ${s}`).join("\n")}\n\nDigite o número ou o nome da especialidade.`;
  }

  if (num === "2" || intent === "CANCEL") {
    return handleCancellingStart(conv, phone);
  }

  if (num === "3" || intent === "STATUS") {
    return handleStatus(conv, phone);
  }

  if (num === "4" || intent === "WAITING_LIST") {
    await setState(conv.id, "WAITING_LIST", {});
    const specialties = await getSpecialties();
    return `Fila de espera 📋\n\nQual especialidade você precisa?\n\n${specialties.map((s, i) => `*${i + 1}.* ${s}`).join("\n")}`;
  }

  if (num === "5" || intent === "SUPPORT") {
    await setState(conv.id, "SUPPORT", {});
    return `Entendido! Vou registrar sua mensagem para nossa equipe entrar em contato em breve. 🙏\n\nPode descrever sua dúvida ou pedido?`;
  }

  return buildMenuMessage(conv.patient?.name);
}

async function handleSchedulingSpecialty(
  conv: WhatsAppConversation & { patient: Patient | null },
  message: string,
  phone: string,
  ctx: Record<string, unknown>
): Promise<string> {
  const specialties = await getSpecialties();
  let specialty = specialties[parseInt(message) - 1] ?? message.trim();

  const professionals = await prisma.professional.findMany({
    where: {
      clinicId: CLINIC_ID,
      isActive: true,
      specialty: { contains: specialty, mode: "insensitive" },
    },
  });

  if (!professionals.length) {
    return `Não encontrei profissionais para "${specialty}". 😕\n\nEspecialidades disponíveis:\n${specialties.map((s, i) => `*${i + 1}.* ${s}`).join("\n")}\n\nDigite novamente:`;
  }

  if (professionals.length === 1) {
    await setState(conv.id, "SCHEDULING_DATE", {
      specialty,
      professionalId: professionals[0].id,
      professionalName: professionals[0].name,
    });
    return `*${professionals[0].name}* (${professionals[0].specialty})\n\nQual *data* você prefere para a consulta?\n\nEx: "amanhã", "próxima segunda", "15/02" ou uma data de sua preferência.`;
  }

  await setState(conv.id, "SCHEDULING_PROFESSIONAL", { specialty });
  return `Profissionais disponíveis em ${specialty}:\n\n${professionals.map((p, i) => `*${i + 1}.* ${p.name}`).join("\n")}\n\nQual você prefere?`;
}

async function handleSchedulingProfessional(
  conv: WhatsAppConversation & { patient: Patient | null },
  message: string,
  phone: string,
  ctx: Record<string, unknown>
): Promise<string> {
  const specialty = ctx.specialty as string;
  const professionals = await prisma.professional.findMany({
    where: { clinicId: CLINIC_ID, isActive: true, specialty: { contains: specialty, mode: "insensitive" } },
  });

  const idx = parseInt(message) - 1;
  const prof = professionals[idx] ?? professionals.find((p) => p.name.toLowerCase().includes(message.toLowerCase()));

  if (!prof) {
    return `Não entendi. Digite o *número* do profissional da lista acima.`;
  }

  await setState(conv.id, "SCHEDULING_DATE", {
    specialty,
    professionalId: prof.id,
    professionalName: prof.name,
  });

  return `*${prof.name}* selecionado! ✅\n\nQual *data* você prefere?\n\nEx: "amanhã", "próxima segunda", "15/02"`;
}

async function handleSchedulingDate(
  conv: WhatsAppConversation & { patient: Patient | null },
  message: string,
  phone: string,
  ctx: Record<string, unknown>
): Promise<string> {
  const extracted = await extractInfo(message, ["date"]);
  let dateStr = extracted.date;

  if (!dateStr) {
    // Tenta interpretar com Claude
    const res = await anthropic.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 20,
      system: `Hoje é ${format(new Date(), "yyyy-MM-dd")}. Converta a expressão de data para ISO (YYYY-MM-DD). Retorne APENAS a data.`,
      messages: [{ role: "user", content: message }],
    });
    dateStr = (res.content[0] as { text: string }).text.trim();
  }

  if (!dateStr || dateStr === "null") {
    return `Não entendi a data. 😕\n\nPode tentar de outro jeito?\nEx: "amanhã", "próxima segunda", "20/03"`;
  }

  const date = parseISO(dateStr);
  const dayOfWeek = date.getDay();

  const slots = await prisma.timeSlot.findMany({
    where: {
      professionalId: ctx.professionalId as string,
      dayOfWeek,
      isActive: true,
    },
    orderBy: { startTime: "asc" },
  });

  if (!slots.length) {
    return `O profissional não tem horários disponíveis em ${format(date, "EEEE, dd/MM", { locale: ptBR })}. 😕\n\nTente outra data:`;
  }

  // Filtra horários já agendados nesse dia
  const booked = await prisma.appointment.findMany({
    where: {
      professionalId: ctx.professionalId as string,
      dateTime: { gte: startOfDay(date), lte: endOfDay(date) },
      status: { in: ["SCHEDULED", "CONFIRMED"] },
    },
    select: { dateTime: true },
  });

  const bookedTimes = booked.map((a) => format(a.dateTime, "HH:mm"));
  const available = slots.filter((s) => !bookedTimes.includes(s.startTime));

  if (!available.length) {
    return `Não há horários livres em ${format(date, "dd/MM", { locale: ptBR })}. 😕\n\nDeseja entrar na *fila de espera* ou escolher outra data?\n\n*1.* Outra data\n*2.* Fila de espera`;
  }

  await setState(conv.id, "SCHEDULING_TIME", { ...ctx, date: dateStr, availableSlots: available.map((s) => s.startTime) });

  const list = available.slice(0, 10).map((s, i) => `*${i + 1}.* ${s}`).join("\n");
  return `Horários disponíveis para ${format(date, "EEEE, dd/MM", { locale: ptBR })}:\n\n${list}\n\nQual horário prefere?`;
}

async function handleSchedulingTime(
  conv: WhatsAppConversation & { patient: Patient | null },
  message: string,
  phone: string,
  ctx: Record<string, unknown>
): Promise<string> {
  const availableSlots = ctx.availableSlots as string[];
  const idx = parseInt(message) - 1;
  const time = availableSlots[idx] ?? message.trim();

  if (!availableSlots.includes(time)) {
    return `Horário inválido. Digite o *número* do horário da lista.`;
  }

  const [h, m] = time.split(":").map(Number);
  const date = parseISO(ctx.date as string);
  date.setHours(h, m, 0, 0);

  await setState(conv.id, "SCHEDULING_CONFIRM", { ...ctx, time, dateTime: date.toISOString() });

  const dateLabel = format(date, "EEEE, dd/MM/yyyy 'às' HH:mm", { locale: ptBR });
  return `Confirme o agendamento:\n\n👨‍⚕️ *${ctx.professionalName}*\n📅 ${dateLabel}\n\nDigite *CONFIRMAR* para agendar ou *CANCELAR* para desistir.`;
}

async function handleSchedulingConfirm(
  conv: WhatsAppConversation & { patient: Patient | null },
  message: string,
  phone: string,
  ctx: Record<string, unknown>
): Promise<string> {
  const intent = await detectIntent(message);
  if (!/confirm|sim|ok|yes|1/i.test(message) && intent !== "CONFIRM") {
    if (/cancel|não|nao|2/i.test(message)) {
      await setState(conv.id, "MENU", {});
      return `Tudo bem! Agendamento cancelado. 😊\n\n${buildMenuMessage(conv.patient?.name)}`;
    }
    return `Digite *CONFIRMAR* para agendar ou *CANCELAR* para desistir.`;
  }

  if (!conv.patientId) {
    await setState(conv.id, "MENU", {});
    return `Ocorreu um erro. Por favor, tente novamente digitando *menu*.`;
  }

  const dateTime = new Date(ctx.dateTime as string);

  const appointment = await prisma.appointment.create({
    data: {
      clinicId: CLINIC_ID,
      professionalId: ctx.professionalId as string,
      patientId: conv.patientId,
      dateTime,
      status: "SCHEDULED",
    },
  });

  // Agenda lembrete 24h antes
  const reminderTime = addHours(dateTime, -24);
  const jobId = await scheduleReminder(appointment.id, reminderTime);

  if (jobId) {
    await prisma.appointment.update({
      where: { id: appointment.id },
      data: { reminderJobId: jobId },
    });
  }

  await setState(conv.id, "MENU", {});

  const dateLabel = format(dateTime, "EEEE, dd/MM/yyyy 'às' HH:mm", { locale: ptBR });
  return `✅ *Consulta agendada com sucesso!*\n\n👨‍⚕️ ${ctx.professionalName}\n📅 ${dateLabel}\n\nVocê receberá um lembrete 24h antes. 😊\n\nDigite *menu* para voltar ao início.`;
}

async function handleCancellingStart(
  conv: WhatsAppConversation & { patient: Patient | null },
  phone: string
): Promise<string> {
  if (!conv.patientId) {
    return `Não encontrei seu cadastro. Digite *menu* para reiniciar.`;
  }

  const appointments = await prisma.appointment.findMany({
    where: {
      patientId: conv.patientId,
      status: { in: ["SCHEDULED", "CONFIRMED"] },
      dateTime: { gte: new Date() },
    },
    include: { professional: true },
    orderBy: { dateTime: "asc" },
    take: 5,
  });

  if (!appointments.length) {
    await setState(conv.id, "MENU", {});
    return `Você não tem consultas agendadas. 😊\n\n${buildMenuMessage(conv.patient?.name)}`;
  }

  await setState(conv.id, "CANCELLING", { appointments: appointments.map((a) => a.id) });

  const list = appointments
    .map((a, i) => `*${i + 1}.* ${format(a.dateTime, "dd/MM/yyyy HH:mm")} - ${a.professional.name}`)
    .join("\n");

  return `Suas consultas agendadas:\n\n${list}\n\nQual deseja cancelar? (Digite o número)`;
}

async function handleCancelling(
  conv: WhatsAppConversation & { patient: Patient | null },
  message: string,
  phone: string,
  ctx: Record<string, unknown>
): Promise<string> {
  const ids = ctx.appointments as string[];
  const idx = parseInt(message) - 1;

  if (isNaN(idx) || !ids[idx]) {
    return `Digite o número da consulta que deseja cancelar.`;
  }

  const appointment = await prisma.appointment.findUnique({
    where: { id: ids[idx] },
    include: { professional: true },
  });

  if (!appointment) {
    return `Consulta não encontrada. Digite *menu* para voltar.`;
  }

  await setState(conv.id, "CANCELLING_CONFIRM", { appointmentId: ids[idx] });

  const dateLabel = format(appointment.dateTime, "dd/MM/yyyy 'às' HH:mm", { locale: ptBR });
  return `Confirma o cancelamento?\n\n👨‍⚕️ ${appointment.professional.name}\n📅 ${dateLabel}\n\nDigite *SIM* para cancelar ou *NÃO* para manter.`;
}

async function handleCancellingConfirm(
  conv: WhatsAppConversation & { patient: Patient | null },
  message: string,
  phone: string,
  ctx: Record<string, unknown>
): Promise<string> {
  if (!/sim|yes|1/i.test(message)) {
    await setState(conv.id, "MENU", {});
    return `Consulta mantida! 😊\n\n${buildMenuMessage(conv.patient?.name)}`;
  }

  const { cancelReminder: cancelJob } = await import("./queue");
  await cancelJob(ctx.appointmentId as string);

  await prisma.appointment.update({
    where: { id: ctx.appointmentId as string },
    data: { status: "CANCELLED" },
  });

  await setState(conv.id, "MENU", {});
  return `✅ Consulta cancelada com sucesso.\n\nSe precisar reagendar, estou à disposição! 😊\n\n${buildMenuMessage(conv.patient?.name)}`;
}

async function handleWaitingList(
  conv: WhatsAppConversation & { patient: Patient | null },
  message: string,
  phone: string,
  ctx: Record<string, unknown>
): Promise<string> {
  if (!ctx.specialty) {
    const specialties = await getSpecialties();
    const idx = parseInt(message) - 1;
    const specialty = specialties[idx] ?? message.trim();

    if (!conv.patientId) {
      await setState(conv.id, "MENU", {});
      return `Não encontrei seu cadastro. Digite *menu* para reiniciar.`;
    }

    await prisma.waitingList.create({
      data: {
        clinicId: CLINIC_ID,
        patientId: conv.patientId,
        specialty,
      },
    });

    await setState(conv.id, "MENU", {});
    return `✅ Você foi adicionado(a) à fila de espera para *${specialty}*!\n\nAssim que houver disponibilidade, entraremos em contato. 😊\n\n${buildMenuMessage(conv.patient?.name)}`;
  }

  await setState(conv.id, "MENU", {});
  return buildMenuMessage(conv.patient?.name);
}

async function handleStatus(
  conv: WhatsAppConversation & { patient: Patient | null },
  phone: string
): Promise<string> {
  if (!conv.patientId) {
    return `Não encontrei seu cadastro. Digite *menu* para reiniciar.`;
  }

  const appointments = await prisma.appointment.findMany({
    where: {
      patientId: conv.patientId,
      dateTime: { gte: new Date() },
      status: { in: ["SCHEDULED", "CONFIRMED"] },
    },
    include: { professional: true },
    orderBy: { dateTime: "asc" },
    take: 3,
  });

  if (!appointments.length) {
    return `Você não tem consultas agendadas. 📅\n\nDigite *1* para agendar uma consulta.`;
  }

  const list = appointments
    .map((a) => {
      const status = a.status === "CONFIRMED" ? "✅ Confirmada" : "🕐 Aguardando confirmação";
      return `📅 ${format(a.dateTime, "dd/MM/yyyy HH:mm")} - ${a.professional.name}\n${status}`;
    })
    .join("\n\n");

  await setState(conv.id, "MENU", {});
  return `Suas próximas consultas:\n\n${list}\n\nDigite *menu* para voltar.`;
}

// ──────────────────────────────────────────────
// HELPERS
// ──────────────────────────────────────────────

async function setState(
  id: string,
  state: ConversationState,
  context: Record<string, unknown>
) {
  await prisma.whatsAppConversation.update({
    where: { id },
    data: { state, context },
  });
}

async function getSpecialties(): Promise<string[]> {
  const result = await prisma.professional.findMany({
    where: { clinicId: CLINIC_ID, isActive: true },
    select: { specialty: true },
    distinct: ["specialty"],
  });
  return result.map((r) => r.specialty);
}

function buildMenuMessage(name?: string | null): string {
  const greeting = name ? `Olá, *${name}*! 😊` : `Olá! 😊`;
  return `${greeting} Como posso ajudar?\n\n*1.* 📅 Agendar consulta\n*2.* ❌ Cancelar consulta\n*3.* 🔍 Minhas consultas\n*4.* ⏳ Fila de espera\n*5.* 💬 Falar com atendente\n\nDigite o número ou descreva o que precisa.`;
}
