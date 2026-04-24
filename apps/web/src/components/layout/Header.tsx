"use client";

import Image from "next/image";
import { signOut } from "next-auth/react";
import { Bell, LogOut, ChevronDown } from "lucide-react";
import { useState } from "react";

interface Props {
  user?: { name?: string | null; email?: string | null; image?: string | null };
}

export default function Header({ user }: Props) {
  const [open, setOpen] = useState(false);

  return (
    <header className="h-16 bg-white border-b border-gray-100 flex items-center justify-between px-6 shadow-sm">
      <div />
      <div className="flex items-center gap-4">
        <button className="relative p-2 text-gray-400 hover:text-gray-600 transition-colors">
          <Bell className="w-5 h-5" />
        </button>

        <div className="relative">
          <button
            onClick={() => setOpen(!open)}
            className="flex items-center gap-2 hover:bg-gray-50 rounded-lg px-2 py-1.5 transition-colors"
          >
            {user?.image ? (
              <Image src={user.image} alt="" width={32} height={32} className="rounded-full" />
            ) : (
              <div className="w-8 h-8 bg-cyan-100 rounded-full flex items-center justify-center">
                <span className="text-cyan-700 font-semibold text-sm">
                  {user?.name?.[0]?.toUpperCase() ?? "U"}
                </span>
              </div>
            )}
            <span className="text-sm font-medium text-gray-700">{user?.name?.split(" ")[0]}</span>
            <ChevronDown className="w-4 h-4 text-gray-400" />
          </button>

          {open && (
            <div className="absolute right-0 top-full mt-1 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-1 z-50">
              <div className="px-3 py-2 border-b border-gray-100">
                <p className="text-sm font-medium text-gray-900 truncate">{user?.name}</p>
                <p className="text-xs text-gray-500 truncate">{user?.email}</p>
              </div>
              <button
                onClick={() => signOut({ callbackUrl: "/login" })}
                className="w-full flex items-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
              >
                <LogOut className="w-4 h-4" />
                Sair
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
