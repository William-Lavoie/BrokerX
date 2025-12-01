"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [portfolio, setPortfolio] = useState(null);

  useEffect(() => {
      const token = localStorage.getItem("access_token");

    fetch("http://localhost:8005/portfolio", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => setPortfolio(data.portfolio))
      .catch((err) => console.error(err));
  }, []);

  if (!portfolio) return <p>Loading portfolio...</p>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>Portfolio Overview</h2>

      <div style={{ marginBottom: "15px" }}>
        <strong>Client ID:</strong> {portfolio.client_id}
      </div>

      <div style={{ marginBottom: "15px" }}>
        <strong>Total Value:</strong> ${portfolio.value}
      </div>

      <div style={{ marginBottom: "15px" }}>
        <strong>Performance:</strong> {portfolio.performance}%
      </div>

        <h3 style={{ marginTop: "30px" }}>Holdings</h3>

      {portfolio.holdings.length === 0 ? (
        <p>No holdings available.</p>
      ) : (
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            marginTop: "10px",
          }}
        >
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Name</th>
              <th>Qty</th>
              <th>Buy Price</th>
              <th>Current Price</th>
              <th>Performance</th>
            </tr>
          </thead>

          <tbody>
            {portfolio.holdings.map((h, index) => (
              <tr key={index}>
                <td >{h.symbol}</td>
                <td >{h.name}</td>
                <td >{h.quantity}</td>
                <td >
                  {h.buying_price !== null ? `$${h.buying_price}` : "-"}
                </td>
                <td >
                  {h.current_price !== null ? `$${h.current_price}` : "-"}
                </td>
                <td >
                  {h.performance !== null ? `${h.performance}%` : "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
