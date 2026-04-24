import { auth } from "@/lib/auth";
import { prisma } from "@/lib/db";
import { startOfDay, endOfDay, startOfMonth, endOfMonth } from "date-fns";
import {
  Calendar,
  Users,
  CheckCircle,
  Clock,
  TrendingUp,
  AlertCircle,
} from "lucide-react";
import Link from "next/link";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

const CLINIC_ID = process.env.CLINIC_ID ?? "default";

export default async function DashboardPage() {
  const session = await auth();
  const now = new Date();
  const todayStart = startOfDay(now);
  const todayEnd = endOfDay(now);
  const monthStart = startOfMonth(now);
  const monthEnd = endOfMonth(now);

  const isProfessional = session?.user?.role === "PROFESSIONAL";

  // Busca profissional logado se for PROFESSIONAL
  let professionalId: string | undefined;
  if (isProfessional && session?.user?.id) {
    const prof = await prisma.professional.findUnique({
      where: { userId: session.user.id },
      select: { id: true },
    });
    professionalId = prof?.id;
  }

  const baseWhere = {
    clinicId: CLINIC_ID,
    ...(professionalId ? { professionalId } : {}),
  };

  const [todayTotal, todayConfirmed, monthTotal, waitingCount, nextAppointments] =
    await Promise.all([
      prisma.appointment.count({
        where: { ...baseWhere, dateTime: { gte: todayStart, lte: todayEnd } },
      }),
      prisma.appointment.count({
        where: {
          ...baseWhere,
          dateTime: { gte: todayStart, lte: todayEnd },
          status: "CONFIRMED",
        },
      }),
      prisma.appointment.count({
        where: {
          ...baseWhere,
          dateTime: { gte: monthStart, lte: monthEnd },
          status: { notIn: ["CANCELLED"] },
        },
      }),
      prisma.waitingList.count({ where: { clinicId: CLINIC_ID, notified: false } }),
      prisma.appointment.findMany({
        where: {
          ...baseWhere,
          dateTime: { gte: now },
          status: { in: ["SCHEDULED", "CONFIRMED"] },
        },
        include: {
          patient: { select: { name: true } },
          professional: { select: { name: true, specialty: true } },
        },
        orderBy: { dateTime: "asc" },
        take: 5,
      }),
    ]);

  const stats = [
    { label: "Consultas hoje", value: todayTotal, icon: Calendar, color: "text-blue-600", bg: "bg-blue-50" },
    { label: "Confirmadas hoje", value: todayConfirmed, icon: CheckCircle, color: "text-green-600", bg: "bg-green-50" },
    { label: "Consultas no mês", value: monthTotal, icon: TrendingUp, color: "text-purple-600", bg: "bg-purple-50" },
    { label: "Fila de espera", value: waitingCount, icon: Clock, color: "text-orange-600", bg: "bg-orange-50" },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 text-sm mt-1">
          {format(now, "EEEE, dd 'de' MMMM 'de' yyyy", { locale: ptBR })}
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.label} className="bg-white rounded-xl border border-gray-100 p-5 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-1">{stat.value}</p>
                </div>
                <div className={`${stat.bg} p-3 rounded-xl`}>
                  <Icon className={`w-6 h-6 ${stat.color}`} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Próximas consultas */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm">
        <div className="p-5 border-b border-gray-100 flex items-center justify-between">
          <h2 className="font-semibold text-gray-900">Próximas Consultas</h2>
          <Link href="/agenda" className="text-sm text-cyan-600 hover:underline">Ver agenda completa</Link>
        </div>

        {nextAppointments.length === 0 ? (
          <div className="p-10 text-center text-gray-400">
            <Calendar className="w-10 h-10 mx-auto mb-3 opacity-40" />
            <p>Nenhuma consulta agendada.</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-50">
            {nextAppointments.map((apt) => (
              <div key={apt.id} className="p-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
                <div className="flex items-center gap-4">
                  <div className="text-center w-14 bg-cyan-50 rounded-lg p-2">
                    <p className="text-xs text-cyan-600 font-medium">
                      {format(apt.dateTime, "dd/MM")}
                    </p>
                    <p className="text-sm font-bold text-cyan-700">
                      {format(apt.dateTime, "HH:mm")}
                    </p>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900 text-sm">{apt.patient.name}</p>
                    <p className="text-xs text-gray-500">{apt.professional.name} · {apt.professional.specialty}</p>
                  </div>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                  apt.status === "CONFIRMED"
                    ? "bg-green-100 text-green-700"
                    : "bg-yellow-100 text-yellow-700"
                }`}>
                  {apt.status === "CONFIRMED" ? "Confirmada" : "Agendada"}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
