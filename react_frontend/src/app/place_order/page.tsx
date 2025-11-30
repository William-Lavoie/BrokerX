"use client"

import { useEffect, useState } from "react"
import { toast } from "react-toastify";

export default function Wallet() {

    const token = localStorage.getItem("access_token");
    const [orders, setOrders] = useState<Order[]>([]);
    const [orderType, setOrderType] = useState("MARKET");
    const [orderDuration, setOrderDuration] = useState("DAY");

    // Edit modal state
    const [editingOrder, setEditingOrder] = useState<Order | null>(null);
    const [editOrderType, setEditOrderType] = useState("MARKET");
    const [editOrderDuration, setEditOrderDuration] = useState("DAY");

    // only PENDING or partially executed orders may be edited
    const isEditable = (order: Order | null): boolean => {
        if (!order || !order.status) return false;
        const s = String(order.status).toUpperCase();
        return s === "PENDING" || s.includes("PARTIAL");
    };

    // map statuses to badge color classes
    const getStatusClasses = (status?: string) => {
        const s = String(status ?? "").toUpperCase();
        if (s === "PENDING") return "bg-blue-100 text-blue-800";
        if (s.includes("PARTIAL")) return "bg-yellow-100 text-yellow-800";
        if (s.includes("CANCEL")) return "bg-red-100 text-red-800";
        if (s.includes("COMPLETE") || s.includes("EXECUTED")) return "bg-green-100 text-green-800";
        return "bg-gray-100 text-gray-700";
    };

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

    const openEdit = (order: Order) => {
        if (!isEditable(order)) {
            toast.error("Only pending or partially executed orders can be edited.", { position: "top-right", autoClose: 4000 });
            return;
        }
        setEditingOrder(order);
        // order_style may be string or array; pick first if array
        const style = Array.isArray(order.order_style) ? String(order.order_style[0] ?? "MARKET") : String(order.order_style ?? "MARKET");
        setEditOrderType(style);
        setEditOrderDuration(order.order_duration ?? "DAY");
    };

    const cancelEdit = () => {
        setEditingOrder(null);
    };

    async function update_order(event: React.FormEvent<HTMLFormElement>): Promise<void> {
        event.preventDefault();
        if (!editingOrder) return;
        if (!isEditable(editingOrder)) {
            toast.error("Order can no longer be edited.", { position: "top-right", autoClose: 4000 });
            setEditingOrder(null);
            return;
        }
        try {
            const form = event.currentTarget;
            const formData = new FormData(form);

            const payload: any = {
                order_id: editingOrder.order_id,
                symbol: formData.get("symbol"),
                quantity: Number(formData.get("quantity")),
                order_type: formData.get("direction"),
                order_style: editOrderType,
                order_duration: editOrderDuration,
            };

            const price = formData.get("price") || null;
            const gtd_date = formData.get("gtd_date") || null;
            if (price !== null) payload.price = Number(price);
            if (gtd_date !== null) payload.end_date = gtd_date;


            const response = await fetch("http://localhost:8002/order", {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json",
                    "Idempotency-Key": editingOrder.order_id,
                },
                body: JSON.stringify(payload),
            });

            const data = await response.json();
            if (!response.ok) {
                const message = data.message || "Failed to update order. Please try again.";
                toast.error(message, { position: "top-right", autoClose: 5000 });
                return;
            }

            // backend might return data.order or data.orders array; normalize
            const updatedOrder = data.order ?? (Array.isArray(data.orders) ? data.orders[0] : null);
            if (updatedOrder) {
                setOrders((prev) => prev.map((o) => (o.order_id === updatedOrder.order_id ? updatedOrder : o)));
            }

            toast.success(data.message || "Order updated successfully!", { position: "top-right", autoClose: 5000 });
            setEditingOrder(null);
        } catch (error) {
            toast.error("There was an unexpected error.", { position: "top-right", autoClose: 5000 });
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
            
            {editingOrder && (
                <div className="fixed inset-0 z-50 flex items-center justify-center">
                    <div className="absolute inset-0 bg-black opacity-40" onClick={cancelEdit} />
                    <form onSubmit={update_order} className="relative bg-white rounded-lg shadow-lg p-6 w-full max-w-2xl z-10">
                        <h3 className="text-lg font-semibold mb-4">Edit Order #{editingOrder.order_id ?? "—"}</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label htmlFor="symbol_edit" className="block text-sm font-medium text-gray-700 mb-1">Symbol</label>
                                <input id="symbol_edit" name="symbol" type="text" required defaultValue={editingOrder.symbol} className="w-full px-3 py-2 border rounded-lg" />
                            </div>
                            <div>
                                <label htmlFor="direction_edit" className="block text-sm font-medium text-gray-700 mb-1">Direction</label>
                                <select id="direction_edit" name="direction" aria-label="Direction" required defaultValue={editingOrder.order_type} className="w-full px-3 py-2 border rounded-lg">
                                    <option value="BUY">Buy</option>
                                    <option value="SELL">Sell</option>
                                </select>
                            </div>
                            <div>
                                <label htmlFor="quantity_edit" className="block text-sm font-medium text-gray-700 mb-1">Quantity</label>
                                <input id="quantity_edit" name="quantity" type="number" placeholder="0" required defaultValue={editingOrder.quantity} className="w-full px-3 py-2 border rounded-lg" />
                            </div>
                            <div>
                                <label htmlFor="duration_edit" className="block text-sm font-medium text-gray-700 mb-1">Duration</label>
                                <select id="duration_edit" name="duration" aria-label="Duration" value={editOrderDuration} onChange={(e) => setEditOrderDuration(e.target.value)} className="w-full px-3 py-2 border rounded-lg">
                                    <option value="DAY">DAY</option>
                                    <option value="IOC">IOC</option>
                                    <option value="FOK">FOK</option>
                                    <option value="GTC">GTC</option>
                                    <option value="GTD">GTD</option>
                                </select>
                            </div>
                            <div className="flex items-center gap-3">
                                <input id="limit-switch-edit" type="checkbox" checked={editOrderType === "LIMIT"} onChange={(e) => setEditOrderType(e.target.checked ? "LIMIT" : "MARKET")} className="h-5 w-5 text-indigo-600 border-gray-300 rounded" />
                                <label htmlFor="limit-switch-edit" className="text-sm text-gray-700">Limit</label>
                            </div>
                            {editOrderType === "LIMIT" && (
                                <div>
                                    <label htmlFor="price_edit" className="block text-sm font-medium text-gray-700 mb-1">Price</label>
                                    <input id="price_edit" name="price" type="number" placeholder="0.00" step="0.01" defaultValue={editingOrder.price ?? ""} className="w-full px-3 py-2 border rounded-lg" />
                                </div>
                            )}
                            {editOrderDuration === "GTD" && (
                                <div>
                                    <label htmlFor="gtd_date_edit" className="block text-sm font-medium text-gray-700 mb-1">GTD Date</label>
                                    <input id="gtd_date_edit" name="gtd_date" type="date" defaultValue={editingOrder.end_date ?? ""} className="w-full px-3 py-2 border rounded-lg" />
                                </div>
                            )}
                        </div>
                        <div className="mt-4 flex justify-end gap-3">
                            <button type="button" onClick={cancelEdit} className="px-4 py-2 bg-gray-200 rounded-lg">Cancel</button>
                            <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">Update</button>
                        </div>
                    </form>
                </div>
            )}
            
            <div className="mt-6">
				<h2 className="text-lg font-bold mb-3">Your Orders</h2>
				{orders.length === 0 && <p className="text-sm text-gray-500">No orders found.</p>}

				<div className="mt-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
					{orders.map((order, i) => (
						<article key={i} className="bg-white border rounded-xl shadow-sm p-4 flex flex-col justify-between">
							<div>
								<div className="flex items-start justify-between gap-3">
									<div>
										<div className="text-xs text-gray-400">Order #{order.order_id ?? "—"}</div>
										<div className="text-lg font-semibold text-slate-900">{order.symbol}</div>
									</div>
									<div className={`text-xs font-medium px-2 py-1 rounded-full ${getStatusClasses(order.status)}`}>
										{order.status}
									</div>
								</div>

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
										<dt className="text-xs text-gray-400">Quantity</dt>
										<dd>{order.quantity}</dd>
									</div>
									<div>
										<dt className="text-xs text-gray-400">Quantity executed</dt>
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

                            <div className="mt-4 flex items-center justify-between">
                                <div className="text-sm text-gray-500">Updated: {order.updated_at ?? "—"}</div>
                                <div className="flex items-center">
                                    {isEditable(order) && (
                                        <button
                                            className="ml-2 bg-blue-500 text-white px-3 py-1 rounded-lg hover:bg-blue-600"
                                            onClick={() => openEdit(order)}
                                        >
                                            Edit
                                        </button>
                                    )}
                                    <button
                                        className="ml-2 bg-red-500 text-white px-3 py-1 rounded-lg hover:bg-red-600"
                                        onClick={() => handleDelete(order.order_id)}
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
						</article>
 					))}
 				</div>
 			</div>
 		</>
 	 )
 }