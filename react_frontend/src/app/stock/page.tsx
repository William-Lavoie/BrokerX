"use client";
import React, { useEffect, useState } from "react";

type StockData = any;

export default function StockPage() {
	const [symbol, setSymbol] = useState<string | null>(null);
	const [data, setData] = useState<StockData | null>(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		// read symbol from query string
		const params = new URLSearchParams(window.location.search);
		const s = params.get("symbol")?.trim() || null;
		setSymbol(s);
	}, []);

	useEffect(() => {
		if (!symbol) return;
		setLoading(true);
		setError(null);
		setData(null);

		const fetchData = async () => {
			try {
				const resp = await fetch(`http://localhost:8004/stock?symbol=${encodeURIComponent(symbol)}`);
				if (!resp.ok) {
					throw new Error(`Server returned ${resp.status}`);
				}
				const json = await resp.json();
				setData(json);
			} catch (err: any) {
				setError(err?.message || "Failed to fetch stock data");
			} finally {
				setLoading(false);
			}
		};

		fetchData();
	}, [symbol]);

	return (
		<div className="p-4">
			<h1 className="text-2xl font-semibold mb-4">Stock details</h1>


			{symbol && (
				<div>
					<p className="mb-2">Symbol: <strong>{symbol}</strong></p>

					{loading && <p>Loading...</p>}

					{error && <p className="text-red-600">Error: {error}</p>}

					{data && (
						<div className="bg-gray-50 p-3 rounded border">
							{/* Basic rendering: show known fields if present, otherwise dump JSON */}
							{(data.price || data.latestPrice || data.current) ? (
								<div className="mb-2">
									<p>Price: <strong>{data.price ?? data.latestPrice ?? data.current}</strong></p>
									{data.change !== undefined && <p>Change: {String(data.change)}</p>}
								</div>
							) : null}

							{/* Fallback: show raw JSON */}
							<pre className="text-sm overflow-auto">{JSON.stringify(data, null, 2)}</pre>
						</div>
					)}
				</div>
			)}
		</div>
	);
}