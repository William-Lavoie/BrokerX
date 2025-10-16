"use client";

import { useEffect, useState } from "react";
import { keycloak } from "@/app/keycloak";

export default function Home() {
  const [username, setUsername] = useState("Loading...");

  useEffect(() => {

    keycloak.init({ onLoad: "login-required",  checkLoginIframe: false, }).then((authenticated) => {
      if (authenticated) {

        const parsedToken = keycloak.tokenParsed;
        const preferredUsername = parsedToken?.preferred_username || "Unknown user";
        setUsername(preferredUsername);
      } else {
        console.warn("User is not authenticated");
      }
    }).catch((err) => {
      console.error("Keycloak init error:", err);
    });
  }, []);

  return (
    <main>
      <h1>Welcome, {username}</h1>
    </main>
  );
}
