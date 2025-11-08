"use client"

import React, { useState } from 'react';
import { InputOtp } from 'primereact/inputotp';
import "./validate_passcode.css"



export default function App() {
  const [otp, setOtp] = useState('');
  const token = localStorage.getItem("access_token");

  async function validate_passcode() {
    try {
      const response = await fetch("http://localhost:8001/passcode", {
          method: "POST",
          headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
          },
          body: JSON.stringify({"passcode" :otp}),
      });

    if (!response.ok) {
        throw new Error("Login failed");
    }

    } catch (error) {
        console.error(error);
    }
  }

  async function generate_passcode() {
    try {
      const response = await fetch("http://localhost:8001/passcode", {
          method: "PUT",
          headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
          },
      });

    if (!response.ok) {
        throw new Error("Login failed");
    }

    } catch (error) {
        console.error(error);
    }
  }


  return (
    <div className="flex flex-column align-items-center">
      <p className="font-bold text-xl mb-2">Authenticate Your Account</p>
      <p className="text-color-secondary block mb-5">Please enter the code sent to your phone.</p>
        <InputOtp
          value={otp}
          onChange={(e) => setOtp(String(e.value ?? ''))}
          length={6}
          style={{ aspectRatio: '1 / 1' }}
          integerOnly
        />
        <div className="flex justify-content-between mt-5 align-self-stretch">
        <button type='reset' onClick={(e) => setOtp("")}>Reset</button>
        <button type='submit' onClick={generate_passcode}>Send a new passcode</button>
        <button type="submit" onClick={validate_passcode}>Submit</button>
      </div>
    </div>
  );
}