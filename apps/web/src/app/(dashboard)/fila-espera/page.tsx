import { prisma } from "@/lib/db";
import { auth } from "@/lib/auth";
import { formatPhone } from "@/lib/utils";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { ClipboardList } from "lucide-react";

const CLINIC_ID = process.env.CLINIC_ID ?? "default";

export default async function FilaEsperaPage() {
  const session = await auth();

  const list = await prisma.waitingList.findMany({
    where: { clinicId: CLINIC_ID, notified: false },
    include: {
      patient: { select: { name: true, phone: true } },
      professional: { select: { name: true, specialty: true } },
    },
    orderBy: { requestedAt: "asc" },
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Fila de Espera</h1>
        <span className="text-sm text-gray-400">{list.length} aguardando</span>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        {list.length === 0 ? (
          <div className="p-10 text-center text-gray-400">
            <ClipboardList className="w-10 h-10 mx-auto mb-3 opacity-40" />
            <p>Nenhum paciente na fila de espera.</p>
          </div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-100">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Posição</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Paciente</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Especialidade</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Solicitado em</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {list.map((item, idx) => (
                <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-3">
                    <span className="w-7 h-7 rounded-full bg-cyan-100 text-cyan-700 font-bold text-sm flex items-center justify-center">
                      {idx + 1}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-sm font-medium text-gray-900">{item.patient.name}</p>
                    <p className="text-xs text-gray-400">{formatPhone(item.patient.phone)}</p>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">
                    {item.specialty ?? item.professional?.specialty ?? "—"}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">
                    {format(item.requestedAt, "dd/MM/yyyy HH:mm", { locale: ptBR })}
                  </td>
                  <td className="px-4 py-3">
                    <form method="POST" action={`/api/waiting-list?id=${item.id}`}>
                      <button
                        type="submit"
                        className="text-xs bg-green-100 text-green-700 px-3 py-1.5 rounded-lg hover:bg-green-200 transition-colors font-medium"
                      >
                        Notificado
                      </button>
                    </form>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
