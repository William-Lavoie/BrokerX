"use client"

import { TextInput } from "@/components/forms";
import { useEffect, useState } from "react"

export default function Wallet() {

    const [funds, setFunds] = useState(0.0)
    const token = localStorage.getItem("access_token");

    useEffect(() => {
      fetch('http://localhost:8002/wallet', {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
      })
        .then(response => response.json())
        .then(json => setFunds(json["balance"]))
        .catch(error => console.error(error));
    }, []);

    async function add_funds(event: React.FormEvent<HTMLFormElement>): Promise<void> {
        event.preventDefault();
        try {

            const form = event.currentTarget;
            const formData = new FormData(form);

            const idempotencyKey = crypto.randomUUID();

            const response = await fetch("http://localhost:8002/wallet", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json",
                    "Idempotency-Key": idempotencyKey,
                },
                body: JSON.stringify({"amount": formData.get("amount")}),
            });

            if (!response.ok) {
                throw new Error("");
            }

            const data = await response.json();

        } catch (error) {
            console.error(error);
        }
    }


    return (
        <>
            <div>Funds available: {funds}$</div>
            <form onSubmit={add_funds}>
                <TextInput name="amount" type="decimal" label="Add funds"></TextInput>
                <button>Submit</button>
            </form>
        </>
    )
}