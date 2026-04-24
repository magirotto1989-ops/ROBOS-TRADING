import { auth } from "@/lib/auth";
import { prisma } from "@/lib/db";
import { startOfWeek, endOfWeek, addDays, format } from "date-fns";
import { ptBR } from "date-fns/locale";

const CLINIC_ID = process.env.CLINIC_ID ?? "default";

const STATUS_LABELS: Record<string, { label: string; class: string }> = {
  SCHEDULED: { label: "Agendada", class: "bg-yellow-100 text-yellow-700" },
  CONFIRMED: { label: "Confirmada", class: "bg-green-100 text-green-700" },
  CANCELLED: { label: "Cancelada", class: "bg-red-100 text-red-700" },
  COMPLETED: { label: "Realizada", class: "bg-blue-100 text-blue-700" },
  NO_SHOW: { label: "Não compareceu", class: "bg-gray-100 text-gray-600" },
};

export default async function AgendaPage({ searchParams }: { searchParams: { date?: string; professionalId?: string } }) {
  const session = await auth();
  const now = searchParams.date ? new Date(searchParams.date) : new Date();
  const weekStart = startOfWeek(now, { locale: ptBR });
  const weekEnd = endOfWeek(now, { locale: ptBR });

  let professionalFilter = searchParams.professionalId;
  if (session?.user?.role === "PROFESSIONAL") {
    const prof = await prisma.professional.findUnique({
      where: { userId: session.user.id },
      select: { id: true },
    });
    professionalFilter = prof?.id;
  }

  const [appointments, professionals] = await Promise.all([
    prisma.appointment.findMany({
      where: {
        clinicId: CLINIC_ID,
        dateTime: { gte: weekStart, lte: weekEnd },
        ...(professionalFilter ? { professionalId: professionalFilter } : {}),
      },
      include: {
        patient: { select: { name: true, phone: true } },
        professional: { select: { id: true, name: true, specialty: true } },
      },
      orderBy: { dateTime: "asc" },
    }),
    prisma.professional.findMany({
      where: { clinicId: CLINIC_ID, isActive: true },
      select: { id: true, name: true, specialty: true },
    }),
  ]);

  const weekDays = Array.from({ length: 7 }, (_, i) => addDays(weekStart, i));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Agenda</h1>
        <div className="text-sm text-gray-500">
          {format(weekStart, "dd/MM")} – {format(weekEnd, "dd/MM/yyyy")}
        </div>
      </div>

      {/* Filtro de profissional */}
      {session?.user?.role !== "PROFESSIONAL" && (
        <div className="flex gap-2 flex-wrap">
          <a
            href="/agenda"
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${!searchParams.professionalId ? "bg-cyan-500 text-white" : "bg-white border text-gray-600 hover:bg-gray-50"}`}
          >
            Todos
          </a>
          {professionals.map((p) => (
            <a
              key={p.id}
              href={`/agenda?professionalId=${p.id}`}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${searchParams.professionalId === p.id ? "bg-cyan-500 text-white" : "bg-white border text-gray-600 hover:bg-gray-50"}`}
            >
              {p.name}
            </a>
          ))}
        </div>
      )}

      {/* Grade semanal */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="grid grid-cols-7 border-b border-gray-100">
          {weekDays.map((day) => (
            <div key={day.toISOString()} className="p-3 text-center border-r border-gray-100 last:border-0">
              <p className="text-xs text-gray-400 uppercase">
                {format(day, "EEE", { locale: ptBR })}
              </p>
              <p className={`text-sm font-semibold mt-0.5 w-7 h-7 flex items-center justify-center rounded-full mx-auto ${
                format(day, "yyyy-MM-dd") === format(new Date(), "yyyy-MM-dd")
                  ? "bg-cyan-500 text-white"
                  : "text-gray-900"
              }`}>
                {format(day, "d")}
              </p>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-7 min-h-64">
          {weekDays.map((day) => {
            const dayApts = appointments.filter(
              (a) => format(a.dateTime, "yyyy-MM-dd") === format(day, "yyyy-MM-dd")
            );
            return (
              <div key={day.toISOString()} className="border-r border-gray-50 last:border-0 p-2 space-y-1.5">
                {dayApts.map((apt) => {
                  const s = STATUS_LABELS[apt.status] ?? STATUS_LABELS.SCHEDULED;
                  return (
                    <div key={apt.id} className="rounded-lg p-2 bg-cyan-50 border border-cyan-100">
                      <p className="text-xs font-semibold text-cyan-800">
                        {format(apt.dateTime, "HH:mm")}
                      </p>
                      <p className="text-xs text-gray-700 truncate">{apt.patient.name}</p>
                      <p className="text-xs text-gray-400 truncate">{apt.professional.name}</p>
                      <span className={`text-xs px-1.5 py-0.5 rounded-full ${s.class} mt-1 inline-block`}>
                        {s.label}
                      </span>
                    </div>
                  );
                })}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
