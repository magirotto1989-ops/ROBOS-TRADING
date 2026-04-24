import { NextRequest, NextResponse } from "next/server";
import { handleWhatsAppMessage } from "@/lib/chatbot";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    // Evolution API webhook payload
    const event = body.event as string;
    if (event !== "messages.upsert") return NextResponse.json({ ok: true });

    const message = body.data;
    if (!message || message.key?.fromMe) return NextResponse.json({ ok: true });

    // Ignora mensagens de grupo
    const remoteJid = message.key?.remoteJid as string;
    if (!remoteJid || remoteJid.includes("@g.us")) return NextResponse.json({ ok: true });

    const phone = remoteJid.replace("@s.whatsapp.net", "").replace(/\D/g, "");
    const text =
      message.message?.conversation ??
      message.message?.extendedTextMessage?.text ??
      message.message?.buttonsResponseMessage?.selectedDisplayText ??
      null;

    if (!text || !phone) return NextResponse.json({ ok: true });

    // Process async (don't block webhook response)
    handleWhatsAppMessage(phone, text).catch(console.error);

    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error("Webhook error:", err);
    return NextResponse.json({ error: "Internal error" }, { status: 500 });
  }
}
