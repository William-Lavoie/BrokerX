"use client"

import React, { useEffect, useState, useRef } from 'react';
import "./validate_passcode.css"
import { toast } from 'react-toastify';



export default function App() {
	const [otp, setOtp] = useState('');
	const token = (typeof window !== 'undefined') ? localStorage.getItem("access_token") : null;

	const [loadingValidate, setLoadingValidate] = useState(false);
	const [loadingGenerate, setLoadingGenerate] = useState(false);
	const [resendTimer, setResendTimer] = useState(0);
	const timerRef = useRef<number | null>(null);

	useEffect(() => {
		return () => {
			if (timerRef.current) {
				clearInterval(timerRef.current);
			}
		};
	}, []);

	async function validate_passcode() {
		if (!otp || otp.length < 6) {
			toast.error("Please enter the 6-digit passcode.");
			return;
		}
		setLoadingValidate(true);
		try {
			const response = await fetch("http://localhost:8001/passcode", {
				method: "POST",
				headers: {
					"Authorization": `Bearer ${token}`,
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ "passcode": otp }),
			});

			if (!response.ok) {
				const data = await response.json().catch(() => ({}));
				if (response.status === 422 && data?.message) {
					toast.error(data.message);
				} else {
					toast.error(data?.message || "Failed to validate passcode.");
				}
				setLoadingValidate(false);
				return;
			}

			toast.success("Passcode validated. Account authenticated.");
			window.location.href = "http://localhost:3000/";
		} catch (error) {
			console.error(error);
			toast.error("Network error. Please try again.");
		} finally {
			setLoadingValidate(false);
		}
	}

	async function generate_passcode() {
		// prevent generating while cooling down
		if (resendTimer > 0) return;
		setLoadingGenerate(true);
		try {
			const response = await fetch("http://localhost:8080/passcode", {
				method: "PUT",
				headers: {
					"Authorization": `Bearer ${token}`,
					"Content-Type": "application/json",
				},
			});

			if (!response.ok) {
				const data = await response.json().catch(() => ({}));
				throw new Error(data?.message || "Failed to send passcode.");
			}

			toast.success((await response.json()).message || "New passcode sent.");
			setResendTimer(60); // 60 second cooldown
			// start timer
			timerRef.current = window.setInterval(() => {
				setResendTimer(prev => {
					if (prev <= 1) {
						if (timerRef.current) {
							clearInterval(timerRef.current);
							timerRef.current = null;
						}
						return 0;
					}
					return prev - 1;
				});
			}, 1000);

		} catch (error) {
			console.error(error);
			toast.error((error as Error).message || "Could not send passcode.");
		} finally {
			setLoadingGenerate(false);
		}
	}

	return (
		<div className="vp-page">
			<div className="vp-card">
				<h1 className="vp-title">Authenticate Your Account</h1>
				<p className="vp-subtitle">Enter the 6-digit code sent to your email/phone to complete account verification.</p>

				<div className="vp-otp-wrap" aria-label="Passcode input">
					<input
						className="vp-code-input"
            required={true}
						value={otp}
						onChange={(e) => {
							// accept up to 6 digits, strip non-digits
							const digits = e.target.value.replace(/\D/g, '').slice(0, 6);
							setOtp(digits);
						}}
						maxLength={6}
						inputMode="numeric"
						pattern="\d*"
						aria-label="6 digit passcode"
						onPaste={(e) => {
							const paste = (e.clipboardData || window.clipboardData).getData('text');
							const digits = paste.replace(/\D/g, '').slice(0, 6);
							if (digits) {
								e.preventDefault();
								setOtp(digits);
							}
						}}
					/>
				</div>

				<div className="vp-actions">
					<button
						type="button"
						className="vp-btn vp-btn-ghost"
						onClick={() => setOtp("")}
						disabled={loadingValidate || loadingGenerate}
						aria-disabled={loadingValidate || loadingGenerate}
					>
						Reset
					</button>

					<button
						type="button"
						className="vp-btn vp-btn-secondary"
						onClick={generate_passcode}
						disabled={loadingGenerate || resendTimer > 0}
						aria-disabled={loadingGenerate || resendTimer > 0}
					>
						{loadingGenerate ? "Sending..." : (resendTimer > 0 ? `Resend in ${resendTimer}s` : "Send a new passcode")}
					</button>

					<button
						type="button"
						className="vp-btn vp-btn-primary"
						onClick={validate_passcode}
						disabled={loadingValidate}
						aria-disabled={loadingValidate}
					>
						{loadingValidate ? "Verifying..." : "Submit"}
					</button>
				</div>

			</div>
		</div>
	);
}