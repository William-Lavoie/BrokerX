"use client"

import { TextInput } from "@/components/forms";
import { useEffect, useState } from "react"

export default function Wallet() {

    const [funds, setFunds] = useState(0.0)
    const token = localStorage.getItem("access_token");

    useEffect(() => {
      fetch('http://localhost:8000/get_funds/', {
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

    return (
        <>
            <div>Funds available: {funds}$</div>
            <form>
                <TextInput type="decimal" label="Add funds"></TextInput>
                <button>Submit</button>
            </form>
        </>
    )
}