import { prisma } from "./index";

async function main() {
  // Clínica principal
  const clinic = await prisma.clinic.upsert({
    where: { id: "default" },
    update: {},
    create: {
      id: "default",
      name: "Clínica Saúde Total",
      phone: "5511999990000",
      whatsapp: "5511999990000",
      address: "Rua das Flores, 123",
      city: "São Paulo",
    },
  });

  // Usuário admin
  const adminUser = await prisma.user.upsert({
    where: { email: "admin@clinica.com" },
    update: {},
    create: {
      email: "admin@clinica.com",
      name: "Administrador",
      role: "ADMIN",
    },
  });

  // Profissional de exemplo
  const profUser = await prisma.user.upsert({
    where: { email: "dr.joao@clinica.com" },
    update: {},
    create: {
      email: "dr.joao@clinica.com",
      name: "Dr. João Silva",
      role: "PROFESSIONAL",
    },
  });

  const professional = await prisma.professional.upsert({
    where: { userId: profUser.id },
    update: {},
    create: {
      userId: profUser.id,
      clinicId: clinic.id,
      name: "Dr. João Silva",
      specialty: "Clínico Geral",
      crm: "CRM/SP 123456",
    },
  });

  // Horários disponíveis (Seg-Sex, 08:00-17:00, slots de 30min)
  const weekdays = [1, 2, 3, 4, 5];
  const slots = [];
  for (let hour = 8; hour < 17; hour++) {
    for (const min of [0, 30]) {
      const start = `${String(hour).padStart(2, "0")}:${String(min).padStart(2, "0")}`;
      const endMin = min + 30;
      const endHour = endMin >= 60 ? hour + 1 : hour;
      const end = `${String(endHour).padStart(2, "0")}:${String(endMin % 60).padStart(2, "0")}`;
      slots.push({ startTime: start, endTime: end });
    }
  }

  for (const day of weekdays) {
    for (const slot of slots) {
      await prisma.timeSlot.upsert({
        where: {
          professionalId_dayOfWeek_startTime: {
            professionalId: professional.id,
            dayOfWeek: day,
            startTime: slot.startTime,
          },
        },
        update: {},
        create: {
          professionalId: professional.id,
          dayOfWeek: day,
          startTime: slot.startTime,
          endTime: slot.endTime,
          durationMin: 30,
        },
      });
    }
  }

  console.log("Seed concluído:", { clinic: clinic.name, professional: professional.name });
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
