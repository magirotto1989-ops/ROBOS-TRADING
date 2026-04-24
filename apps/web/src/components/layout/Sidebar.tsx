"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Calendar,
  Users,
  UserCog,
  ClipboardList,
  MessageSquare,
  Settings,
} from "lucide-react";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard, roles: ["ADMIN", "RECEPTIONIST", "PROFESSIONAL"] },
  { href: "/agenda", label: "Agenda", icon: Calendar, roles: ["ADMIN", "RECEPTIONIST", "PROFESSIONAL"] },
  { href: "/pacientes", label: "Pacientes", icon: Users, roles: ["ADMIN", "RECEPTIONIST"] },
  { href: "/profissionais", label: "Profissionais", icon: UserCog, roles: ["ADMIN"] },
  { href: "/fila-espera", label: "Fila de Espera", icon: ClipboardList, roles: ["ADMIN", "RECEPTIONIST"] },
  { href: "/whatsapp", label: "WhatsApp", icon: MessageSquare, roles: ["ADMIN"] },
  { href: "/configuracoes", label: "Configurações", icon: Settings, roles: ["ADMIN"] },
];

interface Props {
  role: string;
}

export default function Sidebar({ role }: Props) {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-white border-r border-gray-100 flex flex-col shadow-sm">
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-cyan-500 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">C</span>
          </div>
          <div>
            <p className="font-semibold text-gray-900 text-sm">Clínica Saúde Total</p>
            <p className="text-xs text-gray-400">Sistema de Gestão</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        {navItems
          .filter((item) => item.roles.includes(role))
          .map((item) => {
            const Icon = item.icon;
            const active = pathname === item.href || pathname.startsWith(item.href + "/");
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all",
                  active
                    ? "bg-cyan-50 text-cyan-700"
                    : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                )}
              >
                <Icon className={cn("w-4 h-4", active ? "text-cyan-600" : "text-gray-400")} />
                {item.label}
              </Link>
            );
          })}
      </nav>
    </aside>
  );
}
