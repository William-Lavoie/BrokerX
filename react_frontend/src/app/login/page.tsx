"use client";

import { useState } from "react";
import { TextInput } from "@/components/forms";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e: { preventDefault: () => void; }) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8001/api/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: email, // or "email" if your backend expects email
          password,
        }),
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      const data = await response.json();

      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);

      alert("Login successful!");
      window.location.href = "http://localhost:3000"


    } catch (error) {
      console.error(error);
      alert("Login failed. Please check your credentials.");
    }
  };

  return (
    <div className="flex justify-center items-center h-full">
      <div className="md:border md:rounded-xl w-[60%] h-[60%] p-4">
        <form className="flex flex-col gap-y-8 items-center" onSubmit={handleSubmit}>
          <TextInput
            label="Email"
            handler={(e) => setEmail(e.target.value)}
          />
          <TextInput
            label="Password"
            type="password"
            handler={(e) => setPassword(e.target.value)}
          />
          <button className="bg-blue-500 w-1/3 h-10 rounded-xl" type="submit">
            Submit
          </button>
        </form>
        <a href="/create_account">I don&apos;t have an account</a>
      </div>
    </div>
  );
}
