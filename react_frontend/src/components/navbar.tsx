/* eslint-disable @next/next/no-img-element */
"use client"

import { Button, Dropdown, Form } from 'react-bootstrap';
import ProfileDropdown from "./profile_picture";

async function get_stock_info(event: React.FormEvent<HTMLFormElement>): Promise<void> {
        event.preventDefault();
        try {

            const form = event.currentTarget;
            const formData = new FormData(form);
            const symbol = formData.get("symbol");


            const response = await fetch(`http://localhost:8004/stock?symbol=${symbol}`, {
                method: "GET",
            });

            if (!response.ok) {
                throw new Error("");
            }

            const data = await response.json();

        } catch (error) {
            console.error(error);
        }
    }

function NavbarButton({text, route}: {text: string, route: string}) {
    return (
         <div className="w-1/10  flex justify-center items-end">
            <a href={route} className="h-1/3 w-full  bg-white cursor-pointer text-black hover:!bg-blue-500 border-1 flex justify-center items-center rounded-t-md">
                {text}
            </a>
        </div>

    );
}

export function Navbar() {
    return (
        <>
            <nav className="hidden md:flex bg-blue-300 h-[10vh] gap-x-[3%] sticky top-0">
                <img src="/images/default.png"></img>
                <NavbarButton text="Home" route="/" />
                <NavbarButton text="Wallet" route="/wallet" />
                <NavbarButton text="Place Order" route="/place_order" />

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

                <div className="w-1/10  ml-auto">
                    <ProfileDropdown/>
                </div>
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
