"use client"

import { useEffect, useState } from "react";

export default function Home() {
    const [client, setClientInfo] = useState({
      first_name: "",
      last_name: "",
      address: "",
      birth_date: "",
      email: "",
      phone_number: "",
    });
    const token = localStorage.getItem("access_token");


    useEffect(() => {
      fetch('http://localhost:8005/portfolio', {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      })
        .then(response => response.json())
        .then(json => setClientInfo(json))
        .catch(error => console.error(error));
    }, []);

  return (
    <></>
  );
}
