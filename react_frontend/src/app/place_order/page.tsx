"use client"

import { TextInput } from "@/components/forms";
import { useEffect, useState } from "react"
import { FloatingLabel, Form } from "react-bootstrap";

export default function Wallet() {

    const token = localStorage.getItem("access_token");
    const [orders, setOrders] = useState([]);
    const [orderType, setOrderType] = useState("MARKET");
    const [orderDuration, setOrderDuration] = useState("DAY");

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

            if (!response.ok) {
                throw new Error("");
            }

            const data = await response.json();

        } catch (error) {
            console.error(error);
        }
    }


    return (
        <>
            <form onSubmit={place_order} className="d-flex ">
                <div>
                    <FloatingLabel
                        controlId="symbol"
                        label="Symbol"
                        className="mb-3"
                    >
                        <Form.Control name="symbol" type="text" placeholder="name@example.com" />
                    </FloatingLabel>

                    <FloatingLabel controlId="floatingSelect" label="Direction" className="mb-3">
                        <Form.Select name="direction" aria-label="Direction">
                            <option value="BUY">Buy</option>
                            <option value="SELL">Sell</option>
                        </Form.Select>
                    </FloatingLabel>

                    <FloatingLabel
                        controlId="quantity"
                        label="Quantity"
                        className="mb-3"
                    >
                        <Form.Control name="quantity" type="number" placeholder="0"/>
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
                <li key={i} className="border p-2 mb-2 rounded flex justify-between">
                    <span>{order["symbol"]}</span>
                    <span>{order["direction"]}</span>
                    <span>Qty: {order["initial_quantity"]}</span>
                </li>
                ))}
            </ul>
        </>
    )
}