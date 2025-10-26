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
      fetch('http://localhost:8080/client', {
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
    <main className="min-h-screen flex items-center justify-center bg-gray-100 p-6">
      <div className="bg-white shadow-md rounded-lg p-6 w-full max-w-md">
        <h1 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
          Client Information
        </h1>
        <div className="space-y-4">
          <div className="flex justify-between border-b pb-2">
            <span className="font-medium text-gray-600">First Name:</span>
            <span className="text-gray-800">{client.first_name}</span>
          </div>
          <div className="flex justify-between border-b pb-2">
            <span className="font-medium text-gray-600">Last Name:</span>
            <span className="text-gray-800">{client.last_name}</span>
          </div>
          <div className="flex justify-between border-b pb-2">
            <span className="font-medium text-gray-600">Address:</span>
            <span className="text-gray-800 text-right">{client.address}</span>
          </div>
          <div className="flex justify-between border-b pb-2">
            <span className="font-medium text-gray-600">Birth Date:</span>
            <span className="text-gray-800">{client.birth_date}</span>
          </div>
          <div className="flex justify-between border-b pb-2">
            <span className="font-medium text-gray-600">Email:</span>
            <span className="text-gray-800">{client.email}</span>
          </div>
          <div className="flex justify-between">
            <span className="font-medium text-gray-600">Phone Number:</span>
            <span className="text-gray-800">{client.phone_number}</span>
          </div>
        </div>
      </div>
    </main>
  );
}
