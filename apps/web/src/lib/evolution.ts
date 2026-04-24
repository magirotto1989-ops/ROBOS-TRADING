const EVOLUTION_URL = process.env.EVOLUTION_API_URL!;
const EVOLUTION_KEY = process.env.EVOLUTION_API_KEY!;
const INSTANCE = process.env.EVOLUTION_INSTANCE!;

async function request(path: string, body: object) {
  const res = await fetch(`${EVOLUTION_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      apikey: EVOLUTION_KEY,
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Evolution API error ${res.status}: ${text}`);
  }
  return res.json();
}

export async function sendTextMessage(phone: string, text: string) {
  return request(`/message/sendText/${INSTANCE}`, {
    number: phone,
    text,
  });
}

export async function sendButtonMessage(
  phone: string,
  text: string,
  buttons: { id: string; title: string }[]
) {
  return request(`/message/sendButtons/${INSTANCE}`, {
    number: phone,
    title: "Clínica",
    description: text,
    footer: "",
    buttons: buttons.map((b) => ({ buttonId: b.id, buttonText: { displayText: b.title }, type: 1 })),
  });
}

export async function getQrCode() {
  const res = await fetch(`${EVOLUTION_URL}/instance/connect/${INSTANCE}`, {
    headers: { apikey: EVOLUTION_KEY },
  });
  return res.json();
}

export async function createInstance() {
  return request("/instance/create", {
    instanceName: INSTANCE,
    qrcode: true,
    integration: "WHATSAPP-BAILEYS",
  });
}
