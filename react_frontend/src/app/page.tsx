"use client";

import { useEffect, useState } from "react";
import { keycloak } from "./keycloak";

function Stock({symbol, price, quantity, value, change, profit}: {symbol: string, price: number, quantity: number, value: number, change: number, profit: number}) {
  return (
    <tr className="hover:bg-gray-100 border-b-8">
      <td className="font-medium">{symbol}</td>
      <td>{price}</td>
      <td>{value}</td>
      <td>{value}</td>
      <td>{profit}</td>
    </tr>
  )
}

export default function Home() {
  const [username, setUsername] = useState("Loading...");

     useEffect(() => {
    if (keycloak.authenticated && keycloak.tokenParsed) {
      const preferredUsername = keycloak.tokenParsed.preferred_username || "Unknown user";
      setUsername(preferredUsername);
    } else {
      console.warn("User not authenticated or Keycloak not ready");
    }
  }, []);

  return (
    <>
      <h1>Welcome, {username}</h1>
      <div className="w-full flex flex-col items-center">
        <h1 className="font-bold mb-6">Your Portfolio</h1>

        <div className="overflow-x-auto rounded-lg shadow-lg bg-white w-5/7">
          <table className="min-w-full">
            <thead className="bg-gray-200">
              <tr>
                <th>Symbol</th>
                <th>eeeeeee</th>
                <th>Total Value</th>
                <th>Change</th>
                <th>Volume</th>
              </tr>
            </thead>
            <tbody className="">
              <Stock symbol="XEQT" price={38.20} quantity={20} value={764.00} change={2.34} profit={12.34}></Stock>
              <Stock symbol="AAPL" price={150.00} quantity={10} value={1500.00} change={-1.25} profit={50.00}></Stock>
              <Stock symbol="TSLA" price={720.50} quantity={5} value={3602.50} change={15.40} profit={200.00}></Stock>
              <Stock symbol="MSFT" price={280.75} quantity={8} value={2246.00} change={3.50} profit={75.00}></Stock>
              <Stock symbol="GOOGL" price={2520.10} quantity={2} value={5040.20} change={-10.00} profit={100.00}></Stock>
              <Stock symbol="AMZN" price={3400.00} quantity={1} value={3400.00} change={5.00} profit={150.00}></Stock>
              <Stock symbol="NVDA" price={195.60} quantity={15} value={2934.00} change={4.75} profit={120.00}></Stock>
            </tbody>
          </table>
        </div>
      </div>


    </>
  );
}
