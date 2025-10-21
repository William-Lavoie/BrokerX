// app/wallet/page.tsx (or wherever your Wallet page is)

"use client";

import { useEffect, useState } from "react";
import { keycloak } from "../keycloak"; // adjust path as needed
import { TextInput } from "@/components/forms";

export default function Wallet() {
  const [funds, setFunds] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  // Ensure user is authenticated before proceeding
  useEffect(() => {
    if (!keycloak.authenticated) {
      // Trigger login with redirect back to this page
      keycloak.login({
       redirectUri: window.location.origin + window.location.pathname
      });
    } else {
      // Authenticated — fetch wallet data
      const fetchFunds = async () => {
        try {
          await keycloak.updateToken(30);

          const res = await fetch("http://localhost:8000/get_funds/", {
            method: "GET",
            headers: {
              Authorization: `Bearer ${keycloak.token}`,
              "Content-Type": "application/json",
            },
          });

          if (!res.ok) {
            throw new Error(`HTTP error ${res.status}`);
          }

          const data = await res.json();
          setFunds(data.balance);
        } catch (error) {
          console.error("Fetch error:", error);
        } finally {
          setLoading(false);
        }
      };

      fetchFunds();
    }
  }, []);

  if (!keycloak.authenticated || loading || funds === null) {
    return <div>Loading wallet...</div>;
  }

  return (
    <>
      <div>Funds available: {funds.toFixed(2)}$</div>
      <form>
        <TextInput type="decimal" label="Add fefefefeffunds" />
        <button>Submit</button>
      </form>
    </>
  );
}
