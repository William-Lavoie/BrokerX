"use client"

import { useEffect, useState } from "react";

export default function Home() {
    const [data, setData] = useState("Your username");

    useEffect(() => {
      fetch('http://localhost:8000/get_name/')
        .then(response => response.json())
        .then(json => setData(json["name"]))
        .catch(error => console.error(error));
    }, []);
  return (
    <>{data}</>
  );
}
