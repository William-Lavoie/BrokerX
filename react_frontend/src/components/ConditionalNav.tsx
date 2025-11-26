"use client";

import { usePathname } from "next/navigation";
import React from "react";

export default function ConditionalNav({ children }: { children: React.ReactNode }) {
  const pathname = usePathname() || "";
  // hide children for the login route and any sub-routes under /login
  if (pathname.startsWith("/login") || pathname.startsWith("/create_account")) return null;
  return <>{children}</>;
}
