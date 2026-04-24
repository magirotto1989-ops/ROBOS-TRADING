import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import { prisma } from "@/lib/db";

const CLINIC_ID = process.env.CLINIC_ID ?? "default";

export default async function ConfiguracoesPage() {
  const session = await auth();
  if (session?.user?.role !== "ADMIN") redirect("/dashboard");

  const clinic = await prisma.clinic.findUnique({ where: { id: CLINIC_ID } });

  return (
    <div className="space-y-6 max-w-2xl">
      <h1 className="text-2xl font-bold text-gray-900">Configurações</h1>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 space-y-6">
        <div>
          <h2 className="font-semibold text-gray-900 mb-4">Dados da Clínica</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nome</label>
              <input
                defaultValue={clinic?.name ?? ""}
                className="w-full border border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-400"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">WhatsApp</label>
              <input
                defaultValue={clinic?.whatsapp ?? ""}
                placeholder="5511999990000"
                className="w-full border border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-400"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Endereço</label>
              <input
                defaultValue={clinic?.address ?? ""}
                className="w-full border border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-400"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Cidade</label>
              <input
                defaultValue={clinic?.city ?? ""}
                className="w-full border border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-400"
              />
            </div>
          </div>
        </div>

        <div className="pt-4 border-t border-gray-100">
          <button className="bg-cyan-500 text-white px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-cyan-600 transition-colors">
            Salvar alterações
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
        <h2 className="font-semibold text-gray-900 mb-2">Lembretes</h2>
        <p className="text-sm text-gray-500 mb-4">
          Lembretes automáticos são enviados via WhatsApp <strong>24 horas antes</strong> de cada consulta.
        </p>
        <div className="bg-cyan-50 rounded-lg px-4 py-3">
          <p className="text-sm text-cyan-700 font-medium">Ativo — 24h antes via WhatsApp</p>
        </div>
      </div>
    </div>
  );
}
