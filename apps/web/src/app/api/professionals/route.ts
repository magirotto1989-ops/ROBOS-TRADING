import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/db";
import { z } from "zod";

const CLINIC_ID = process.env.CLINIC_ID ?? "default";

const CreateSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
  specialty: z.string().min(2),
  crm: z.string().optional(),
  cro: z.string().optional(),
  phone: z.string().optional(),
  bio: z.string().optional(),
});

export async function GET(req: NextRequest) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const { searchParams } = new URL(req.url);
  const specialty = searchParams.get("specialty");

  const professionals = await prisma.professional.findMany({
    where: {
      clinicId: CLINIC_ID,
      isActive: true,
      ...(specialty ? { specialty: { contains: specialty, mode: "insensitive" } } : {}),
    },
    include: {
      user: { select: { email: true, image: true } },
      _count: { select: { appointments: true } },
    },
    orderBy: { name: "asc" },
  });

  return NextResponse.json(professionals);
}

export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session || session.user?.role !== "ADMIN") {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const body = await req.json();
  const parsed = CreateSchema.safeParse(body);
  if (!parsed.success) return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });

  const user = await prisma.user.upsert({
    where: { email: parsed.data.email },
    update: { name: parsed.data.name, role: "PROFESSIONAL" },
    create: { email: parsed.data.email, name: parsed.data.name, role: "PROFESSIONAL" },
  });

  const professional = await prisma.professional.create({
    data: {
      userId: user.id,
      clinicId: CLINIC_ID,
      name: parsed.data.name,
      specialty: parsed.data.specialty,
      crm: parsed.data.crm,
      cro: parsed.data.cro,
      phone: parsed.data.phone,
      bio: parsed.data.bio,
    },
    include: { user: { select: { email: true } } },
  });

  return NextResponse.json(professional, { status: 201 });
}
