import { prisma } from "@/lib/db";
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import { UserCog, Stethoscope } from "lucide-react";

const CLINIC_ID = process.env.CLINIC_ID ?? "default";

export default async function ProfissionaisPage() {
  const session = await auth();
  if (session?.user?.role !== "ADMIN") redirect("/dashboard");

  const professionals = await prisma.professional.findMany({
    where: { clinicId: CLINIC_ID },
    include: {
      user: { select: { email: true, image: true } },
      _count: { select: { appointments: true, timeSlots: true } },
    },
    orderBy: { name: "asc" },
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Profissionais</h1>
        <span className="text-sm text-gray-400">{professionals.length} cadastrados</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {professionals.map((p) => (
          <div key={p.id} className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-cyan-100 rounded-xl flex items-center justify-center shrink-0">
                {p.user.image ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={p.user.image} alt="" className="w-12 h-12 rounded-xl object-cover" />
                ) : (
                  <span className="text-cyan-700 font-bold text-lg">{p.name[0]}</span>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-gray-900 truncate">{p.name}</p>
                <p className="text-sm text-cyan-600">{p.specialty}</p>
                <p className="text-xs text-gray-400 mt-0.5">{p.crm ?? p.cro ?? p.user.email}</p>
              </div>
              <span className={`text-xs px-2 py-1 rounded-full font-medium ${p.isActive ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-500"}`}>
                {p.isActive ? "Ativo" : "Inativo"}
              </span>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-2 pt-4 border-t border-gray-50">
              <div className="text-center">
                <p className="text-lg font-bold text-gray-900">{p._count.appointments}</p>
                <p className="text-xs text-gray-400">Consultas</p>
              </div>
              <div className="text-center">
                <p className="text-lg font-bold text-gray-900">{p._count.timeSlots}</p>
                <p className="text-xs text-gray-400">Horários</p>
              </div>
            </div>
          </div>
        ))}

        {professionals.length === 0 && (
          <div className="col-span-3 py-16 text-center text-gray-400">
            <UserCog className="w-12 h-12 mx-auto mb-3 opacity-40" />
            <p>Nenhum profissional cadastrado.</p>
          </div>
        )}
      </div>
    </div>
  );
}
