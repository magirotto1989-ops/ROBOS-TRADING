import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/db";

const CLINIC_ID = process.env.CLINIC_ID ?? "default";

export async function GET(req: NextRequest) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const list = await prisma.waitingList.findMany({
    where: { clinicId: CLINIC_ID, notified: false },
    include: {
      patient: { select: { id: true, name: true, phone: true } },
      professional: { select: { id: true, name: true, specialty: true } },
    },
    orderBy: { requestedAt: "asc" },
  });

  return NextResponse.json(list);
}

export async function DELETE(req: NextRequest) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const { searchParams } = new URL(req.url);
  const id = searchParams.get("id");
  if (!id) return NextResponse.json({ error: "id required" }, { status: 400 });

  await prisma.waitingList.update({ where: { id }, data: { notified: true, notifiedAt: new Date() } });

  return NextResponse.json({ success: true });
}
