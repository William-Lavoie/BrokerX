"use client"
import { useEffect, useState } from "react";

function NavbarButton({text, route}: {text: string, route: string}) {
    return (
        <a href={route} className="w-1/10 flex justify-center items-center hover:bg-blue-500 cursor-pointer">{text}</a>
    )
}

export function Navbar() {
    const [windowWidth, setWindowWidth] = useState(window.innerWidth);

    useEffect(() => {
        const handleResize = () => {
        setWindowWidth(window.innerWidth);
        };

        window.addEventListener('resize', handleResize);

        return () => {
        window.removeEventListener('resize', handleResize);
        };
    }, []);
    
    return (
        <> {windowWidth < 768 ? 
                <nav className="h-[10vh] flex gap-x-[3%] sticky top-0">
                    <NavbarButton text="Home" route="/"></NavbarButton>
                    <NavbarButton text="Wallet" route="/wallet"></NavbarButton>
                    <NavbarButton text="Place Order" route="/create_account"></NavbarButton>
                    <NavbarButton text="Logout" route="/login"></NavbarButton>
                </nav>
            ?
            <div>Ok</div>
        }
        </>
           
      
    )
}