"use client"

import { useState } from "react"
import { toast } from "react-toastify";

export default function Login() {

    const [email_error, setEmailError] = useState("");
    const [password_error, setPasswordError] = useState("");
    const [password_confirm_error, setConfirmedPasswordError] = useState("");
    const [showPassword, setShowPassword] = useState(false);

    function emailMatch(): void {
        const email = (document.querySelector("#email-input") as HTMLInputElement)?.value;
        const confirmed_email = (document.querySelector("#confirm-email-input") as HTMLInputElement)?.value;

        if (email === confirmed_email || confirmed_email === "") {
            setEmailError("");
        } else {
            setEmailError("The two emails must match");
        }
    }

    function validatePasswords(): void {
        const password = (document.querySelector("#password-input") as HTMLInputElement)?.value;
        const confirm_password = (document.querySelector("#confirm-password-input") as HTMLInputElement)?.value;

        if (password && !password.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).{8,}$")) {
            setPasswordError("The password must have at least 8 characters, one lowercase and one uppercase");
        } else {
            setPasswordError("");
        }

        if (confirm_password && password !== confirm_password) {
            setConfirmedPasswordError("The two passwords must match");
        } else {
            setConfirmedPasswordError("");
        }
    }

    async function create_account(event: React.FormEvent<HTMLFormElement>): Promise<void> {
        event.preventDefault();
        try {

            const form = event.currentTarget;
            const formData = new FormData(form);

            const payload = {
                first_name: formData.get("first-name"),
                last_name: formData.get("last-name"),
                email: formData.get("email"),
                phone_number: formData.get("phone-number"),
                date_of_birth: formData.get("date-of-birth"),
                address: formData.get("address"),
                communication_method: formData.get("communication-method"),
                password: formData.get("password"),
            };
        const response = await fetch("http://localhost:8080/client", {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
             if (response.status === 409) {
                toast.error("An account with this email or phone number already exists. Do you wish to recover your account?");
                return;
            }
            throw new Error("Login failed");
        }

        const data = await response.json();
        if (data["succcess"]) {
            window.location.href = "http://localhost:3000/validate_passcode"
        }

        } catch (error) {
            console.error(error);
        }

    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <div className="bg-white shadow-lg rounded-xl w-full max-w-3xl p-8">
                <div className="flex flex-col items-center gap-4 mb-4">
                    <img src="/images/default.png" alt="BrokerX Logo" className="h-30"/>
                </div>
                <h2 className="text-2xl font-semibold mb-6 text-center">Create an account</h2>

                <form className="grid gap-6" onSubmit={create_account}>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label htmlFor="first-name" className="block text-sm font-medium mb-1">First Name</label>
                            <input id="first-name" name="first-name" type="text" required className="bg-gray-100 w-full p-2 rounded-md border-[var(--color-emerald-700)] focus:outline-none focus:ring-2 focus:ring-[var(--color-emerald-700)] focus:border-[var(--color-emerald-700)]" />
                        </div>
                        <div>
                            <label htmlFor="last-name" className="block text-sm font-medium mb-1">Last Name</label>
                            <input id="last-name" name="last-name" type="text" required className="bg-gray-100 w-full p-2 rounded-md border-[var(--color-emerald-700)] focus:outline-none focus:ring-2 focus:ring-[var(--color-emerald-700)] focus:border-[var(--color-emerald-700)]" />
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label htmlFor="email-input" className="block text-sm font-medium mb-1">Email address</label>
                            <input id="email-input" name="email" type="email" required onChange={emailMatch} className="bg-gray-100 w-full p-2 rounded-md border-[var(--color-emerald-700)] focus:outline-none focus:ring-2 focus:ring-[var(--color-emerald-700)] focus:border-[var(--color-emerald-700)]" />
                        </div>
                        <div>
                            <label htmlFor="confirm-email-input" className="block text-sm font-medium mb-1">Confirm Email</label>
                            <input id="confirm-email-input" name="confirm-email" type="email" required onChange={emailMatch} className="bg-gray-100 w-full p-2 rounded-md border-[var(--color-emerald-700)] focus:outline-none focus:ring-2 focus:ring-[var(--color-emerald-700)] focus:border-[var(--color-emerald-700)]" />
                            <span className="text-red-500 text-sm mt-1 block">{email_error}</span>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label htmlFor="phone-number" className="block text-sm font-medium mb-1">Phone Number</label>
                            <input id="phone-number" name="phone-number" type="tel" required className="bg-gray-100 w-full p-2 rounded-md border-[var(--color-emerald-700)] focus:outline-none focus:ring-2 focus:ring-[var(--color-emerald-700)] focus:border-[var(--color-emerald-700)]" />
                        </div>
                        <div>
                            <label htmlFor="date-of-birth" className="block text-sm font-medium mb-1">Date of Birth</label>
                            <input id="date-of-birth" name="date-of-birth" type="date" required className="bg-gray-100 w-full p-2 rounded-md border-[var(--color-emerald-700)] focus:outline-none focus:ring-2 focus:ring-[var(--color-emerald-700)] focus:border-[var(--color-emerald-700)]" />
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label htmlFor="address" className="block text-sm font-medium mb-1">Address</label>
                            <input id="address" name="address" type="text" required className="bg-gray-100 w-full p-2 rounded-md border-[var(--color-emerald-700)] focus:outline-none focus:ring-2 focus:ring-[var(--color-emerald-700)] focus:border-[var(--color-emerald-700)]" />
                        </div>
                        <div>
                            <label htmlFor="communication-method" className="block text-sm font-medium mb-1">Preferred communication method</label>
                            <select name="communication-method" id="communication-method" required className="bg-gray-100 w-full p-2 rounded-md border-[var(--color-emerald-700)] focus:outline-none focus:ring-2 focus:ring-[var(--color-emerald-700)] focus:border-[var(--color-emerald-700)]">
                                <option>Email</option>
                                <option>SMS</option>
                            </select>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label htmlFor="password-input" className="block text-sm font-medium mb-1">Password</label>
                            <input id="password-input" name="password" type={showPassword ? "text" : "password"} required onChange={validatePasswords} className="bg-gray-100 w-full p-2 rounded-md border-[var(--color-emerald-700)] focus:outline-none focus:ring-2 focus:ring-[var(--color-emerald-700)] focus:border-[var(--color-emerald-700)]" />
                            <span className="text-red-500 text-sm mt-1 block">{password_error}</span>
                        </div>

                        <div>
                            <label htmlFor="confirm-password-input" className="block text-sm font-medium mb-1">Confirm Password</label>
                            <input id="confirm-password-input" name="confirm-password" type={showPassword ? "text" : "password"} required onChange={validatePasswords} className="bg-gray-100 w-full p-2 rounded-md border-[var(--color-emerald-700)] focus:outline-none focus:ring-2 focus:ring-[var(--color-emerald-700)] focus:border-[var(--color-emerald-700)]" />
                            <span className="text-red-500 text-sm mt-1 block">{password_confirm_error}</span>
                        </div>
                    </div>

                    <div className="flex items-center gap-2 text-sm">
                        <input
                            id="show-password"
                            type="checkbox"
                            checked={showPassword}
                            onChange={(e) => setShowPassword(e.target.checked)}
                            className="h-4 w-4 rounded border-[var(--color-emerald-700)] text-[var(--color-emerald-700)] focus:ring-[var(--color-emerald-700)]"
                        />
                        <label htmlFor="show-password" className="text-slate-700">Show password</label>
                    </div>

                    <div className="flex flex-col md:flex-row items-center md:items-center md:justify-between gap-4">
                        <button type="submit" className="bg-emerald-700 text-white py-2 px-6 rounded-lg w-full md:w-auto hover:bg-emerald-800">Create account</button>
                        <div className="flex items-center gap-4">
                            <a href="/login" className="text-sm text-gray-600 hover:underline">Already have an account? Log in</a>
                        </div>
                    </div>
                </form>
            </div>
        </div>


    )
}