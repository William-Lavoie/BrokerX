"use client"

import { useEffect, useState } from "react"
import { toast } from "react-toastify";

export default function Wallet() {
	const [funds, setFunds] = useState<number | null>(null)
 	const [amount, setAmount] = useState<string>("")
 	const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

 	useEffect(() => {
 		async function loadBalance() {
 			try {
 				const res = await fetch("http://localhost:8080/wallet", {
 					method: "GET",
 					headers: {
 						"Authorization": `Bearer ${token}`,
 						"Content-Type": "application/json",
 					},
 				})
 				const json = await res.json()
 				setFunds(json.balance)
 			} catch (err) {
 				console.error(err)
 				toast.error("Failed to load wallet balance.", { position: "top-right", autoClose: 4000 })
 			}
 		}
 		loadBalance()
 	}, [token]);

 	async function add_funds(event: React.FormEvent<HTMLFormElement>): Promise<void> {
		event.preventDefault()

		try {
			const idempotencyKey = (crypto && (crypto as any).randomUUID) ? (crypto as any).randomUUID() : `${Date.now()}-${Math.random()}`

			const response = await fetch("http://localhost:8003/wallet", {
				method: "PUT",
				headers: {
					"Authorization": `Bearer ${token}`,
					"Content-Type": "application/json",
					"Idempotency-Key": idempotencyKey,
				},
				body: JSON.stringify({ amount: Number(amount) }),
			})

			const data = await response.json()

			if (!response.ok) {
				const message = data?.message || "Failed to add funds. Please try again."
				toast.error(message, { position: "top-right", autoClose: 5000 })
				return
			}

			setFunds(data.balance)
			setAmount("")
			toast.success(data?.message || "Funds added successfully!", { position: "top-right", autoClose: 4000 })

		} catch (error) {
			console.error(error)
			toast.error("There was an unexpected error.", { position: "top-right", autoClose: 5000 })
		}
	}

	function formatCurrency(v: number | null) {
		if (v === null) return "—"
		return v.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " $"
	}

	return (
		<div className="min-h-[200px] flex items-center justify-center p-6 mt-40">
			<div className="w-full max-w-md bg-white bg-emerald-400 rounded-xl shadow-md p-6">
				<div className="flex items-center justify-between mb-4">
					<div>
						<div className="text-sm text-gray-500">Wallet balance</div>
						<div className="text-2xl font-semibold text-slate-900">
							{formatCurrency(funds)}
						</div>
					</div>
				</div>

				<form onSubmit={add_funds} className="space-y-3">
					<label className="block text-sm font-medium text-slate-700">Add funds</label>
					<div className="flex gap-2">
						<input
							name="amount"
							type="number"
							step="0.01"
							min="0"
							value={amount}
							onChange={(e) => setAmount(e.target.value)}
							placeholder="0.00"
							className="flex-1 px-3 py-2 border rounded-lg border-gray-200 focus:outline-none focus:ring-1 focus:ring-indigo-400"
							aria-label="Amount to add"
                            required={true}
						/>
						<button
							type="submit"
							className={`px-4 py-2 rounded-lg text-white bg-emerald-700 cursor-not-allowed`}
						>
						Add
						</button>
					</div>
				</form>
			</div>
		</div>
	)
}