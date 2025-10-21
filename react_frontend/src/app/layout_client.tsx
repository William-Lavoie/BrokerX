"use client";

import { Navbar } from "@/components/navbar";
import { ReactNode, useEffect, useRef, useState } from "react";
import { keycloak } from "./keycloak";

function KeycloakInit({ children }: { children: ReactNode }) {
  const [loading, setLoading] = useState(true);
  const hasRun = useRef(false);

  useEffect(() => {
    if (hasRun.current) return;
    hasRun.current = true;

    keycloak
      .init({
        onLoad: "check-sso",
        pkceMethod: "S256",
        checkLoginIframe: false,
        redirectUri: window.location.origin + window.location.pathname,
        responseMode: "query",
      })
      .then((authenticated) => {
        console.log("Keycloak initialized. Authenticated:", authenticated);
        setLoading(false);

        if (window.location.hash) {
          history.replaceState(null, "", window.location.pathname + window.location.search);
        }
      })
      .catch((err) => {
        console.error("Keycloak initialization failed", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading authentication...</div>;

  return <>{children}</>;
}

export default function ClientLayout({ children }: { children: ReactNode }) {
  return (
    <KeycloakInit>
      <Navbar />
      {children}
    </KeycloakInit>
  );
}
