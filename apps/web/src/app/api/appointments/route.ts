import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/db";
import { scheduleReminder, cancelReminder } from "@/lib/queue";
import { addHours } from "date-fns";
import { z } from "zod";

const CLINIC_ID = process.env.CLINIC_ID ?? "default";

const CreateSchema = z.object({
  professionalId: z.string(),
  patientId: z.string(),
  dateTime: z.string().datetime(),
  durationMin: z.number().int().positive().default(30),
  notes: z.string().optional(),
});

export async function GET(req: NextRequest) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const { searchParams } = new URL(req.url);
  const start = searchParams.get("start");
  const end = searchParams.get("end");
  const professionalId = searchParams.get("professionalId");
  const patientId = searchParams.get("patientId");

  const appointments = await prisma.appointment.findMany({
    where: {
      clinicId: CLINIC_ID,
      ...(start && end ? { dateTime: { gte: new Date(start), lte: new Date(end) } } : {}),
      ...(professionalId ? { professionalId } : {}),
      ...(patientId ? { patientId } : {}),
    },
    include: {
      professional: { select: { id: true, name: true, specialty: true } },
      patient: { select: { id: true, name: true, phone: true } },
    },
    orderBy: { dateTime: "asc" },
  });

  return NextResponse.json(appointments);
}

export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const body = await req.json();
  const parsed = CreateSchema.safeParse(body);
  if (!parsed.success) return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });

  const { professionalId, patientId, dateTime, durationMin, notes } = parsed.data;
  const dt = new Date(dateTime);

  // Verifica conflito de horário
  const conflict = await prisma.appointment.findFirst({
    where: {
      professionalId,
      status: { in: ["SCHEDULED", "CONFIRMED"] },
      dateTime: { gte: dt, lt: new Date(dt.getTime() + durationMin * 60000) },
    },
  });

  if (conflict) {
    return NextResponse.json({ error: "Horário já ocupado para este profissional." }, { status: 409 });
  }

  const appointment = await prisma.appointment.create({
    data: { clinicId: CLINIC_ID, professionalId, patientId, dateTime: dt, durationMin, notes, status: "SCHEDULED" },
    include: {
      professional: { select: { name: true } },
      patient: { select: { name: true, phone: true } },
    },
  });

  // Agenda lembrete 24h antes
  const reminderTime = addHours(dt, -24);
  const jobId = await scheduleReminder(appointment.id, reminderTime);
  if (jobId) {
    await prisma.appointment.update({ where: { id: appointment.id }, data: { reminderJobId: jobId } });
  }

  return NextResponse.json(appointment, { status: 201 });
}
