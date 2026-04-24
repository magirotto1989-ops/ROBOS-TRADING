import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/db";
import { z } from "zod";

const CLINIC_ID = process.env.CLINIC_ID ?? "default";

const CreateSchema = z.object({
  name: z.string().min(2),
  phone: z.string().min(10),
  email: z.string().email().optional().nullable(),
  cpf: z.string().optional().nullable(),
  birthDate: z.string().optional().nullable(),
  notes: z.string().optional().nullable(),
});

export async function GET(req: NextRequest) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const { searchParams } = new URL(req.url);
  const q = searchParams.get("q");
  const page = parseInt(searchParams.get("page") ?? "1");
  const limit = parseInt(searchParams.get("limit") ?? "20");

  const where = {
    clinicId: CLINIC_ID,
    ...(q ? {
      OR: [
        { name: { contains: q, mode: "insensitive" as const } },
        { phone: { contains: q } },
        { cpf: { contains: q } },
      ],
    } : {}),
  };

  const [patients, total] = await Promise.all([
    prisma.patient.findMany({
      where,
      orderBy: { name: "asc" },
      skip: (page - 1) * limit,
      take: limit,
      include: { _count: { select: { appointments: true } } },
    }),
    prisma.patient.count({ where }),
  ]);

  return NextResponse.json({ patients, total, page, pages: Math.ceil(total / limit) });
}

export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const body = await req.json();
  const parsed = CreateSchema.safeParse(body);
  if (!parsed.success) return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });

  const phone = parsed.data.phone.replace(/\D/g, "");

  const existing = await prisma.patient.findUnique({
    where: { clinicId_phone: { clinicId: CLINIC_ID, phone } },
  });
  if (existing) return NextResponse.json({ error: "Paciente com este telefone já cadastrado." }, { status: 409 });

  const patient = await prisma.patient.create({
    data: {
      clinicId: CLINIC_ID,
      name: parsed.data.name,
      phone,
      email: parsed.data.email,
      cpf: parsed.data.cpf,
      birthDate: parsed.data.birthDate ? new Date(parsed.data.birthDate) : undefined,
      notes: parsed.data.notes,
    },
  });

  return NextResponse.json(patient, { status: 201 });
}
