import React from "react";

export const metadata = {
  title: "Login",
};

export default function LoginLayout({ children }: { children: React.ReactNode }) {
  // This layout intentionally omits the global navbar/header.
  return <>{children}</>;
}
