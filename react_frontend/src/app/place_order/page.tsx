"use client"

import { TextInput } from "@/components/forms";
import { useEffect, useState } from "react"

export default function Wallet() {

    const token = localStorage.getItem("access_token");

    async function place_order(event: React.FormEvent<HTMLFormElement>): Promise<void> {
        event.preventDefault();
        try {

            const form = event.currentTarget;
            const formData = new FormData(form);

            const payload = {
                symbol: formData.get("symbol"),
                quantity: formData.get("quantity"),
                direction: formData.get("direction"),
            };
            const idempotencyKey = crypto.randomUUID();

            const response = await fetch("http://localhost:8000/order", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json",
                    "Idempotency-Key": idempotencyKey,
                },
                body: JSON.stringify(payload),
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
            <form onSubmit={place_order}>
                <TextInput name="symbol" label="symbol" type="decimal"></TextInput>
                <TextInput name="quantity" type="number" label="Quantity"></TextInput>
                <TextInput name="direction" label="Type" type="text"></TextInput>
                <button>Submit</button>
            </form>
        </>
    )
}