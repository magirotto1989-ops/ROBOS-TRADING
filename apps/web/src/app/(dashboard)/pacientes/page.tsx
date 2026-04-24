import { auth } from "@/lib/auth";
import { prisma } from "@/lib/db";
import { formatPhone } from "@/lib/utils";
import { Users, Phone, Calendar } from "lucide-react";

const CLINIC_ID = process.env.CLINIC_ID ?? "default";

export default async function PacientesPage({ searchParams }: { searchParams: { q?: string; page?: string } }) {
  const session = await auth();
  const q = searchParams.q ?? "";
  const page = parseInt(searchParams.page ?? "1");
  const limit = 20;

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
      include: {
        _count: { select: { appointments: true } },
      },
    }),
    prisma.patient.count({ where }),
  ]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Pacientes</h1>
        <span className="text-sm text-gray-400">{total} cadastrados</span>
      </div>

      {/* Busca */}
      <form className="flex gap-3">
        <input
          name="q"
          defaultValue={q}
          placeholder="Buscar por nome, telefone ou CPF..."
          className="flex-1 border border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-400"
        />
        <button
          type="submit"
          className="bg-cyan-500 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-cyan-600 transition-colors"
        >
          Buscar
        </button>
      </form>

      {/* Lista */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        {patients.length === 0 ? (
          <div className="p-10 text-center text-gray-400">
            <Users className="w-10 h-10 mx-auto mb-3 opacity-40" />
            <p>Nenhum paciente encontrado.</p>
          </div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-100">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Nome</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Telefone</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">CPF</th>
                <th className="px-4 py-3 text-center text-xs font-semibold text-gray-500 uppercase">Consultas</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {patients.map((p) => (
                <tr key={p.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-cyan-100 rounded-full flex items-center justify-center">
                        <span className="text-cyan-700 font-semibold text-xs">{p.name[0]}</span>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-900">{p.name}</p>
                        {p.email && <p className="text-xs text-gray-400">{p.email}</p>}
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-1.5 text-sm text-gray-600">
                      <Phone className="w-3.5 h-3.5 text-gray-400" />
                      {formatPhone(p.phone)}
                    </div>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">{p.cpf ?? "—"}</td>
                  <td className="px-4 py-3 text-center">
                    <span className="inline-flex items-center gap-1 text-xs text-gray-500">
                      <Calendar className="w-3.5 h-3.5" />
                      {p._count.appointments}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Paginação */}
      {total > limit && (
        <div className="flex justify-center gap-2">
          {Array.from({ length: Math.ceil(total / limit) }, (_, i) => i + 1).map((p) => (
            <a
              key={p}
              href={`/pacientes?q=${q}&page=${p}`}
              className={`w-8 h-8 flex items-center justify-center rounded-lg text-sm ${
                p === page ? "bg-cyan-500 text-white" : "bg-white border text-gray-600 hover:bg-gray-50"
              }`}
            >
              {p}
            </a>
          ))}
        </div>
      )}
    </div>
  );
}
