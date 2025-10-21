/* eslint-disable @next/next/no-img-element */
"use client"

import { redirect } from "next/dist/server/api-utils";

function NavbarButton({text, route}: {text: string, route: string}) {
    return (
        <a href={route} className="w-1/10 flex justify-center items-center hover:bg-blue-500 cursor-pointer">
            {text}
        </a>
    );
}

function logout() {
    localStorage.setItem("access_token", "");
    localStorage.setItem("refresh_token", "");
    window.location.href = "http://localhost:3000/login"
}

export function Navbar() {
    return (
        <>
            <nav className="hidden md:flex bg-blue-300 h-[10vh] gap-x-[3%] sticky top-0">
                <img src="/images/default.png"></img>
                <NavbarButton text="Home" route="/" />
                <NavbarButton text="Wallet" route="/wallet" />
                <NavbarButton text="Place Order" route="/create_account/validate_passcode" />
                <button onClick={logout}>Logout</button>
            </nav>

            <nav className="md:hidden bg-blue-300 flex h-[10vh] justify-between pr-[10px] sticky top-0">
                <img src="/images/profile.png"></img>
                <button>
                    <img src="/images/dropdown.svg" alt="Dropdown menu" className="w-[50px]"/>
                </button>
            </nav>

        </>
    );
}
