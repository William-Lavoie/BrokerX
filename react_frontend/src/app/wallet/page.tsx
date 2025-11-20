"use client"

import { TextInput } from "@/components/forms";
import { useEffect, useState } from "react"
import { toast } from "react-toastify";

export default function Wallet() {

    const [funds, setFunds] = useState(0.0)
    const token = localStorage.getItem("access_token");

    useEffect(() => {
      fetch('http://localhost:8003/wallet', {
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

        const response = await fetch("http://localhost:8003/wallet", {
            method: "PUT",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
                "Idempotency-Key": idempotencyKey,
            },
            body: JSON.stringify({ amount: formData.get("amount") }),
        });

        const data = await response.json();


        if (!response.ok) {
            const message = data.message || "Failed to add funds. Please try again.";
            toast.error(message, {
                position: "top-right",
                autoClose: 5000,
            });
            return;
        }

        setFunds(data.balance);
        toast.success(data.message || `Funds added successfully!`, {
            position: "top-right",
            autoClose: 5000,
        });

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (error: any) {
        console.error(error);

        // Show error toast
        toast.error(`There was an unexpected error.`, {
            position: "top-right",
            autoClose: 5000,
        });
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