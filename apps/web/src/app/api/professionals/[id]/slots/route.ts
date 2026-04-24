import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/db";
import { startOfDay, endOfDay, parseISO, format } from "date-fns";

export async function GET(req: NextRequest, { params }: { params: { id: string } }) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const { searchParams } = new URL(req.url);
  const dateStr = searchParams.get("date");
  if (!dateStr) return NextResponse.json({ error: "date required" }, { status: 400 });

  const date = parseISO(dateStr);
  const dayOfWeek = date.getDay();

  const [slots, booked] = await Promise.all([
    prisma.timeSlot.findMany({
      where: { professionalId: params.id, dayOfWeek, isActive: true },
      orderBy: { startTime: "asc" },
    }),
    prisma.appointment.findMany({
      where: {
        professionalId: params.id,
        dateTime: { gte: startOfDay(date), lte: endOfDay(date) },
        status: { in: ["SCHEDULED", "CONFIRMED"] },
      },
      select: { dateTime: true },
    }),
  ]);

  const bookedTimes = new Set(booked.map((a) => format(a.dateTime, "HH:mm")));

  return NextResponse.json(
    slots.map((s) => ({
      ...s,
      available: !bookedTimes.has(s.startTime),
    }))
  );
}
