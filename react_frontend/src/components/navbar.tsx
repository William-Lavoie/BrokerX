/* eslint-disable @next/next/no-img-element */
"use client"

import React, { useEffect, useState } from 'react';
import { Button, Dropdown, Form } from 'react-bootstrap';
import ProfileDropdown from "./profile_picture";

// Add: safe token getter and a global SSE wrapper to avoid multiple connections
const getClientToken = () => {
	// Only access localStorage in browser
	if (typeof window === 'undefined') return '';
	return localStorage.getItem('access_token') || '';
};

type SSEWrapper = {
	source: EventSource;
	listeners: Set<(e: MessageEvent) => void>;
};

declare global {
	interface Window {
		__brokerx_sse?: SSEWrapper;
	}
}

async function get_stock_info(event: React.FormEvent<HTMLFormElement>): Promise<void> {
		event.preventDefault();
		try {
			const form = event.currentTarget;
			const formData = new FormData(form);
			const symbolRaw = formData.get("symbol");
			const symbol = symbolRaw ? String(symbolRaw).trim() : "";

			if (!symbol) {
				// nothing to do
				return;
			}

			// Redirect to a page that will display stock info.
			// The target page can read the symbol from the query and fetch/display details.
			const encoded = encodeURIComponent(symbol);
			window.location.href = `/stock?symbol=${encoded}`;
		} catch (error) {
			console.error(error);
		}
	}

function NavbarButton({text, route}: {text: string, route: string}) {
    return (
         <div className="w-1/10  flex justify-center items-end">
            <a href={route} className="h-1/3 w-full  bg-white cursor-pointer text-black hover:!bg-emerald-500 border-1 flex justify-center items-center rounded-t-md">
                {text}
            </a>
        </div>

    );
}

export function Navbar() {
	const [notifications, setNotifications] = useState<Array<any>>([]);
	const [unreadCount, setUnreadCount] = useState<number>(0);

	useEffect(() => {
		// Use the client token. If missing, don't attempt SSE.
		const token = getClientToken();
		if (!token) {
			console.warn("No access token found for notifications SSE.");
			return;
		}

		// SSE endpoint with token as query param (EventSource cannot send custom headers).
		const sseUrl = `http://localhost:8006/notification?token=${encodeURIComponent(token)}/`;

		// Create global wrapper if it doesn't exist.
		if (!window.__brokerx_sse) {
			const es = new EventSource(sseUrl);
			const wrapper: SSEWrapper = { source: es, listeners: new Set() };

			es.onmessage = (e: MessageEvent) => {
				// dispatch to all registered listeners
				wrapper.listeners.forEach((l) => {
					try { l(e); } catch (err) { console.error("Listener error", err); }
				});
			};

			es.onerror = (err) => {
				console.error("EventSource error:", err);
			};

			window.__brokerx_sse = wrapper;
		} else {
			// Optional: if token changed and backend requires it, you may recreate the source here.
			// For now we reuse the existing connection.
		}

		// local listener for this component instance
		const localHandler = (e: MessageEvent) => {
			try {
				const data = JSON.parse(e.data);
				const entry = {
					id: Date.now().toString(),
					payload: data,
					timestamp: new Date().toLocaleTimeString(),
					read: false,
				};
				setNotifications((prev) => [entry, ...prev]);
				setUnreadCount((c) => c + 1);
			} catch (err) {
				console.error("Invalid notification payload", err);
			}
		};

		window.__brokerx_sse.listeners.add(localHandler);

		// cleanup: remove our listener; if no listeners remain close the source
		return () => {
			if (window.__brokerx_sse) {
				window.__brokerx_sse.listeners.delete(localHandler);
				if (window.__brokerx_sse.listeners.size === 0) {
					window.__brokerx_sse.source.close();
					delete window.__brokerx_sse;
				}
			}
		};
	}, []);

	const markAllRead = () => {
		setNotifications((prev) => prev.map(n => ({ ...n, read: true })));
		setUnreadCount(0);
	};

    return (
        <>
            <nav className="hidden md:flex bg-white h-[10vh] gap-x-[3%] sticky top-0">
                <img src="/images/default.png" alt="logo" />

                <NavbarButton text="Home" route="/" />
                <NavbarButton text="Wallet" route="/wallet" />
                <NavbarButton text="Place Order" route="/place_order" />
                <NavbarButton text="Portfolio" route="/portfolio" />

                <div className="d-flex items-center">
                    <Form className="d-flex h-1/3" onSubmit={get_stock_info}>
                        <Form.Control
                            name="symbol"
                            type="search"
                            placeholder="Search"
                            aria-label="Search"
                            required
                        />
                        <Button variant="outline-success" type='submit'>Search</Button>
                    </Form>
                </div>

				<div className="flex items-center">
					<Dropdown align="end" onToggle={(isOpen) => { if (isOpen) markAllRead(); }}>
						<Dropdown.Toggle variant="light" id="dropdown-notifications" className="relative flex items-center">
							<svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
								<path strokeLinecap="round" strokeLinejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
							</svg>

							{unreadCount > 0 && (
								<span className="absolute -top-1 -right-1 bg-red-600 text-white text-xs rounded-full px-1">
									{unreadCount}
								</span>
							)}
						</Dropdown.Toggle>

						<Dropdown.Menu style={{ minWidth: 300 }}>
							<div className="px-2 py-1 flex justify-between items-center">
								<strong>Notifications</strong>
								<button className="text-sm text-blue-600" onClick={(e) => { e.stopPropagation(); markAllRead(); }}>Mark all read</button>
							</div>
							<Dropdown.Divider />
							{notifications.length === 0 && (
								<Dropdown.ItemText className="text-center text-muted">No notifications</Dropdown.ItemText>
							)}
							{notifications.map((n) => (
								<Dropdown.ItemText key={n.id} className={`px-3 py-2 ${n.read ? 'text-gray-500' : ''}`}>
									<div className="flex justify-between">
										<div>
											<div className="font-medium">{n.payload?.title ?? 'Notification'}</div>
											<div className="text-sm">{n.payload?.message ?? JSON.stringify(n.payload)}</div>
										</div>
										<div className="text-xs text-gray-400 ml-2">{n.timestamp}</div>
									</div>
								</Dropdown.ItemText>
							))}
						</Dropdown.Menu>
					</Dropdown>
				</div>

                <div className="w-1/10  ml-auto">
                    <ProfileDropdown/>
                </div>
            </nav>

            <nav className="md:hidden bg-blue-300 flex h-[10vh] justify-between pr-[10px] sticky top-0">
                <img src="/images/profile.png" alt="profile"></img>
                <button>
                    <img src="/images/dropdown.svg" alt="Dropdown menu" className="w-[50px]"/>
                </button>
            </nav>

        </>
    );
}
