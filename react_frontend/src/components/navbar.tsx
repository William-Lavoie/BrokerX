function NavbarButton({text, route}: {text: string, route: string}) {
    return (
        <a href={route} className="w-1/10 flex justify-center items-center hover:bg-blue-500 cursor-pointer">{text}</a>
    )
}

export function Navbar() {
    return (
        <nav className="h-[10vh] flex gap-x-[3%] sticky top-0">
            <NavbarButton text="Home" route="/"></NavbarButton>
            <NavbarButton text="Wallet" route="/wallet"></NavbarButton>
            <NavbarButton text="Place Order" route="/create_account"></NavbarButton>
            <NavbarButton text="Logout" route="/login"></NavbarButton>
        </nav>
    )
}