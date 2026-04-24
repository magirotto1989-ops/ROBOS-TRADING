import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/db";
import { cancelReminder } from "@/lib/queue";
import { z } from "zod";

const UpdateSchema = z.object({
  status: z.enum(["SCHEDULED", "CONFIRMED", "CANCELLED", "COMPLETED", "NO_SHOW"]).optional(),
  notes: z.string().optional(),
});

export async function PATCH(req: NextRequest, { params }: { params: { id: string } }) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const body = await req.json();
  const parsed = UpdateSchema.safeParse(body);
  if (!parsed.success) return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });

  const current = await prisma.appointment.findUnique({ where: { id: params.id } });
  if (!current) return NextResponse.json({ error: "Not found" }, { status: 404 });

  if (parsed.data.status === "CANCELLED") {
    await cancelReminder(params.id);
  }

  const appointment = await prisma.appointment.update({
    where: { id: params.id },
    data: parsed.data,
    include: {
      professional: { select: { name: true } },
      patient: { select: { name: true, phone: true } },
    },
  });

  return NextResponse.json(appointment);
}

export async function DELETE(req: NextRequest, { params }: { params: { id: string } }) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  await cancelReminder(params.id);
  await prisma.appointment.update({ where: { id: params.id }, data: { status: "CANCELLED" } });

  return NextResponse.json({ success: true });
}
