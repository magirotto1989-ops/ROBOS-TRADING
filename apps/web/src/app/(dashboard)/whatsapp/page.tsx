"use client";

import { useState, useEffect } from "react";
import { MessageSquare, RefreshCw, CheckCircle } from "lucide-react";
import Image from "next/image";

export default function WhatsAppPage() {
  const [qrData, setQrData] = useState<{ base64?: string; status?: string } | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchQr = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/whatsapp/qrcode");
      const data = await res.json();
      setQrData(data);
    } catch {
      setQrData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQr();
    const interval = setInterval(fetchQr, 30000);
    return () => clearInterval(interval);
  }, []);

  const connected = qrData?.status === "open";

  return (
    <div className="space-y-6 max-w-lg">
      <h1 className="text-2xl font-bold text-gray-900">WhatsApp</h1>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-8 text-center">
        {connected ? (
          <div className="space-y-4">
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto" />
            <p className="text-xl font-semibold text-gray-900">WhatsApp Conectado!</p>
            <p className="text-gray-500 text-sm">O chatbot está ativo e recebendo mensagens.</p>
            <div className="bg-green-50 rounded-lg p-3">
              <p className="text-green-700 text-sm font-medium">Status: Online</p>
            </div>
          </div>
        ) : qrData?.base64 ? (
          <div className="space-y-4">
            <MessageSquare className="w-10 h-10 text-cyan-500 mx-auto" />
            <p className="font-semibold text-gray-900">Conecte seu WhatsApp</p>
            <p className="text-sm text-gray-500">
              Abra o WhatsApp no celular → Menu → Dispositivos conectados → Conectar dispositivo
            </p>
            <div className="flex justify-center">
              <Image
                src={qrData.base64}
                alt="QR Code WhatsApp"
                width={240}
                height={240}
                className="rounded-xl border border-gray-100"
              />
            </div>
            <p className="text-xs text-gray-400">QR Code atualiza automaticamente a cada 30s</p>
          </div>
        ) : (
          <div className="space-y-4">
            <MessageSquare className="w-10 h-10 text-gray-300 mx-auto" />
            <p className="text-gray-500">Carregando...</p>
          </div>
        )}

        <button
          onClick={fetchQr}
          disabled={loading}
          className="mt-6 flex items-center gap-2 mx-auto text-sm text-cyan-600 hover:text-cyan-700 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          Atualizar
        </button>
      </div>
    </div>
  );
}
