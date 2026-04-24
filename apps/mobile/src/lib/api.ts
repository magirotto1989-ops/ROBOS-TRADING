import Constants from "expo-constants";

const BASE_URL = Constants.expoConfig?.extra?.apiUrl ?? "http://localhost:3000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: "Unknown error" }));
    throw new Error(error.error ?? `HTTP ${res.status}`);
  }

  return res.json();
}

export type Appointment = {
  id: string;
  dateTime: string;
  status: string;
  durationMin: number;
  notes?: string;
  patient: { id: string; name: string; phone: string };
  professional: { id: string; name: string; specialty: string };
};

export type Professional = {
  id: string;
  name: string;
  specialty: string;
  crm?: string;
  cro?: string;
  isActive: boolean;
};

export const api = {
  appointments: {
    list: (params?: { start?: string; end?: string; professionalId?: string }) => {
      const qs = new URLSearchParams(params as Record<string, string>).toString();
      return request<Appointment[]>(`/api/appointments${qs ? `?${qs}` : ""}`);
    },
    create: (data: { professionalId: string; patientId: string; dateTime: string; durationMin?: number; notes?: string }) =>
      request<Appointment>("/api/appointments", { method: "POST", body: JSON.stringify(data) }),
    update: (id: string, data: { status?: string; notes?: string }) =>
      request<Appointment>(`/api/appointments/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  },
  professionals: {
    list: () => request<Professional[]>("/api/professionals"),
    slots: (id: string, date: string) =>
      request<{ startTime: string; endTime: string; available: boolean }[]>(
        `/api/professionals/${id}/slots?date=${date}`
      ),
  },
};
