import { NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { getQrCode, createInstance } from "@/lib/evolution";

export async function GET() {
  const session = await auth();
  if (!session || session.user?.role !== "ADMIN") {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  try {
    const data = await getQrCode();
    return NextResponse.json(data);
  } catch {
    // Instance may not exist, try to create it
    try {
      await createInstance();
      const data = await getQrCode();
      return NextResponse.json(data);
    } catch (err) {
      return NextResponse.json({ error: "Failed to get QR code" }, { status: 500 });
    }
  }
}
