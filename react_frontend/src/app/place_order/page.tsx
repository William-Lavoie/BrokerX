"use client"

import { useEffect, useState } from "react"
import { toast } from "react-toastify";

export default function Wallet() {

    const token = localStorage.getItem("access_token");
    const [orders, setOrders] = useState<Order[]>([]);
    const [orderType, setOrderType] = useState("MARKET");
    const [orderDuration, setOrderDuration] = useState("DAY");

    interface Order {
        order_id?: string;
        client_id?: string;
        symbol: string;
        order_type: string;
        order_style: string[] | string;
        order_duration: string;
        quantity: number;
        quantity_executed: number;
        price?: number | string;
        end_date?: string;
        status: string;
        created_at?: string;
        updated_at?: string;
        executed_at?: string;
    }
    useEffect(() => {
        fetch("http://localhost:8002/order", {
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        })
        .then((res) => res.json())
        .then((data) => setOrders(data.orders || []))
        .catch(console.error);
    }, [token]);

    async function place_order(event: React.FormEvent<HTMLFormElement>): Promise<void> {
        event.preventDefault();
        try {

            const form = event.currentTarget;
            const formData = new FormData(form);

            type OrderPayload = {
                symbol: FormDataEntryValue | null;
                quantity: number;
                order_type: FormDataEntryValue | null;
                order_style: string;
                order_duration: string;
                price?: number | null;
                end_date?: FormDataEntryValue | null;
            };

            const payload: OrderPayload = {
                symbol: formData.get("symbol"),
                quantity: Number(formData.get("quantity")),
                order_type: formData.get("direction"),
                order_style: orderType,
                order_duration: orderDuration,
            };
            const price = formData.get("price") || null;
            const gtd_date = formData.get("gtd_date") || null;

            if (price !== null) {
                payload.price = Number(price);
            }

            if (gtd_date !== null) {
                payload.end_date = gtd_date;
            }


            const idempotencyKey = crypto.randomUUID();

            const response = await fetch("http://localhost:8002/order", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json",
                    "Idempotency-Key": idempotencyKey,
                },
                body: JSON.stringify(payload),
            });

            const data = await response.json();

            if (!response.ok) {
                const message = data.message || "Failed to place order. Please try again.";
                toast.error(message, {
                    position: "top-right",
                    autoClose: 5000,
                });
                return;
            }
    
            setOrders([...orders, ...data.orders]);

            toast.success(data.message || `Order placed successfully!`, {
                position: "top-right",
                autoClose: 5000,
            });
            
        } catch (error) {
            toast.error(`There was an unexpected error.`, {
            position: "top-right",
            autoClose: 5000,
        });
        }
    }

    const handleDelete = (orderId: string | undefined) => {
        // Remove order from local state
        setOrders((prevOrders) => prevOrders.filter((o) => o.order_id !== orderId));

        // Optionally, call backend API to delete the order
        fetch(`http://localhost:8002/order`, {
            method: "DELETE",
            headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
            },
            body: JSON.stringify({"order_id": orderId})
        })
        .then(async (response) => {
            const data = await response.json();

            if (!response.ok) {
                const message = data.message || "Failed to place order. Please try again.";
                toast.error(message, {
                    position: "top-right",
                    autoClose: 5000,
                });
                return;
            }
    
            toast.success(data.message || `Order placed successfully!`, {
                position: "top-right",
                autoClose: 5000,
            });
        })
        .catch((err) => toast.error(`There was an unexpected error.`, {
            position: "top-right",
            autoClose: 5000,
        }));
    };


    return (
        <>
            <form onSubmit={place_order} className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-white p-6 rounded-lg shadow-md w-1/2 mx-auto mt-10">
                <div className="space-y-4">
                    <div>
                        <label htmlFor="symbol" className="block text-sm font-medium text-gray-700 mb-1">Symbol</label>
                        <input id="symbol" name="symbol" type="text" required className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                    </div>

                    <div>
                        <label htmlFor="direction" className="block text-sm font-medium text-gray-700 mb-1">Direction</label>
                        <select id="direction" name="direction" aria-label="Direction" required className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300">
                            <option value="BUY">Buy</option>
                            <option value="SELL">Sell</option>
                        </select>
                    </div>

                    <div>
                        <label htmlFor="quantity" className="block text-sm font-medium text-gray-700 mb-1">Quantity</label>
                        <input id="quantity" name="quantity" type="number" placeholder="0" required className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                    </div>
                </div>

                <div className="space-y-4">
                    <div>
                        <label htmlFor="duration" className="block text-sm font-medium text-gray-700 mb-1">Duration</label>
                        <select id="duration" name="duration" aria-label="Duration" onChange={(e) => setOrderDuration(e.target.value)} className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300">
                            <option value="DAY">DAY</option>
                            <option value="IOC">IOC</option>
                            <option value="FOK">FOK</option>
                            <option value="GTC">GTC</option>
                            <option value="GTD">GTD</option>
                        </select>
                    </div>

                    <div className="flex items-center gap-3">
                        <input id="limit-switch" type="checkbox" checked={orderType === "LIMIT"} onChange={(e) => setOrderType(e.target.checked ? "LIMIT" : "MARKET")} className="h-5 w-5 text-indigo-600 border-gray-300 rounded" />
                        <label htmlFor="limit-switch" className="text-sm text-gray-700">Limit</label>
                    </div>

                    {orderType === "LIMIT" && (
                        <div>
                            <label htmlFor="price" className="block text-sm font-medium text-gray-700 mb-1">Price</label>
                            <input id="price" name="price" type="number" placeholder="0.00" step="0.01" className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                        </div>
                    )}

                    {orderDuration === "GTD" && (
                        <div>
                            <label htmlFor="gtd_date" className="block text-sm font-medium text-gray-700 mb-1">GTD Date</label>
                            <input id="gtd_date" name="gtd_date" type="date" placeholder="YYYY-MM-DD" className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                        </div>
                    )}
                </div>

                <div className="md:col-span-2 flex justify-end">
                    <button type="submit" className="px-5 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">Submit</button>
                </div>
            </form>
            
            <div className="mt-6">
				<h2 className="text-lg font-bold mb-3">Your Orders</h2>
				{orders.length === 0 && <p className="text-sm text-gray-500">No orders found.</p>}

				{/* responsive grid: 1 column on mobile, 2 on small, 3 on large */}
				<div className="mt-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
					{orders.map((order, i) => (
						<article key={i} className="bg-white border rounded-xl shadow-sm p-4 flex flex-col justify-between">
							{/* header */}
							<div>
								<div className="flex items-start justify-between gap-3">
									<div>
										<div className="text-xs text-gray-400">Order #{order.order_id ?? "—"}</div>
										<div className="text-lg font-semibold text-slate-900">{order.symbol}</div>
										<div className="text-sm text-gray-500">{order.client_id}</div>
									</div>
									<div className={`text-xs font-medium px-2 py-1 rounded-full ${order.status === "COMPLETED" ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-700"}`}>
										{order.status}
									</div>
								</div>

								{/* details grid */}
								<dl className="grid grid-cols-2 gap-x-4 gap-y-2 mt-3 text-sm text-gray-700">
									<div>
										<dt className="text-xs text-gray-400">Type</dt>
										<dd>{order.order_type}</dd>
									</div>
									<div>
										<dt className="text-xs text-gray-400">Style</dt>
										<dd>{Array.isArray(order.order_style) ? order.order_style.join(", ") : order.order_style}</dd>
									</div>
									<div>
										<dt className="text-xs text-gray-400">Duration</dt>
										<dd>{order.order_duration}</dd>
									</div>
									<div>
										<dt className="text-xs text-gray-400">Qty</dt>
										<dd>{order.quantity}</dd>
									</div>
									<div>
										<dt className="text-xs text-gray-400">Exec Qty</dt>
										<dd>{order.quantity_executed}</dd>
									</div>
									<div>
										<dt className="text-xs text-gray-400">Price</dt>
										<dd>{order.price ?? "—"}</dd>
									</div>
									<div>
										<dt className="text-xs text-gray-400">End Date</dt>
										<dd>{order.end_date ?? "—"}</dd>
									</div>
									<div>
										<dt className="text-xs text-gray-400">Created</dt>
										<dd>{order.created_at ?? "—"}</dd>
									</div>
								</dl>
							</div>

							{/* action row */}
							<div className="mt-4 flex items-center justify-between">
								<div className="text-sm text-gray-500">Updated: {order.updated_at ?? "—"}</div>
								<button
									className="ml-4 bg-red-500 text-white px-3 py-1 rounded-lg hover:bg-red-600"
									onClick={() => handleDelete(order.order_id)}
								>
									Delete
								</button>
							</div>
						</article>
					))}
				</div>
			</div>
        </>
     )
 }