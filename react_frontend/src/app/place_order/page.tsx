"use client"

import { TextInput } from "@/components/forms";
import { useEffect, useState } from "react"
import { FloatingLabel, Form } from "react-bootstrap";
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
            <form onSubmit={place_order} className="d-flex ">
                <div>
                    <FloatingLabel
                        controlId="symbol"
                        label="Symbol"
                        className="mb-3"
                    >
                        <Form.Control name="symbol" type="text" placeholder="name@example.com" required />
                    </FloatingLabel>

                    <FloatingLabel controlId="floatingSelect" label="Direction" className="mb-3">
                        <Form.Select name="direction" aria-label="Direction" required>
                            <option value="BUY">Buy</option>
                            <option value="SELL">Sell</option>
                        </Form.Select>
                    </FloatingLabel>

                    <FloatingLabel
                        controlId="quantity"
                        label="Quantity"
                        className="mb-3"
                    >
                        <Form.Control name="quantity" type="number" placeholder="0" required/>
                    </FloatingLabel>

                </div>

                <div>
                    <FloatingLabel controlId="floatingSelect" label="Duration" className="mb-3">
                        <Form.Select name="duration" aria-label="Duration" onChange={(e) => setOrderDuration(e.target.value)}>
                            <option value="DAY">DAY</option>
                            <option value="IOC">IOC</option>
                            <option value="FOK">FOK</option>
                            <option value="GTC">GTC</option>
                            <option value="GTD">GTD</option>
                        </Form.Select>
                    </FloatingLabel>

                    <Form.Check
                        type="switch"
                        id="custom-switch"
                        label="Limit"
                        onChange={(e) => setOrderType(e.target.checked ? "LIMIT" : "MARKET")}
                    />

                    {orderType === "LIMIT" && (
                        <FloatingLabel controlId="price" label="Price" className="mb-3">
                            <Form.Control
                                name="price"
                                type="number"
                                placeholder="0.00"
                                step="0.01"
                            />
                        </FloatingLabel>
                    )}

                    {orderDuration === "GTD" && (
                        <FloatingLabel controlId="gtd_date" label="GTD Date" className="mb-3">
                            <Form.Control
                                name="gtd_date"
                                type="date"
                                placeholder="YYYY-MM-DD"
                            />
                        </FloatingLabel>
                    )}
                </div>

                <button>Submit</button>
            </form>

            <h2 className="text-lg font-bold mb-2">Your Orders</h2>
            {orders.length === 0 && <p>No orders found.</p>}
            <ul>
            {orders.map((order, i) => (
                <li
                key={i}
                className="border p-3 mb-3 rounded bg-white shadow-sm"
                >
                <div className="grid grid-cols-2 gap-2 text-sm">
                    <div><strong>Order ID:</strong> {order.order_id}</div>
                    <div><strong>Client ID:</strong> {order.client_id}</div>

                    <div><strong>Symbol:</strong> {order.symbol}</div>
                    <div><strong>Order Type:</strong> {order.order_type}</div>

                    <div><strong>Order Style:</strong> {Array.isArray(order.order_style) ? order.order_style.join(", ") : order.order_style}</div>
                    <div><strong>Duration:</strong> {order.order_duration}</div>

                    <div><strong>Quantity:</strong> {order.quantity}</div>
                    <div><strong>Executed Qty:</strong> {order.quantity_executed}</div>

                    <div><strong>Price:</strong> {order.price}</div>
                    <div><strong>End Date:</strong> {order.end_date}</div>

                    <div><strong>Status:</strong> {order.status}</div>
                    <div><strong>Created At:</strong> {order.created_at}</div>

                    <div><strong>Updated At:</strong> {order.updated_at}</div>
                    <div><strong>Executed At:</strong> {order.executed_at}</div>
                </div>
                  {/* Delete Button */}
                <button
                    className="ml-4 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                    onClick={() => handleDelete(order.order_id)}
                >
                    Delete
                </button>
                </li>
            ))}
            </ul>
        </>
    )
}