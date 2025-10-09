"use client"

import { useState } from "react"

export function TextInput({label}: {label: string}) {
    const [value, setValue] = useState("")

    return (
        <div className="flex flex-col w-100">
            <label id={value}>{label}</label>
                <input 
                    id={value}
                    className="bg-gray-200 p-2"
                    name={value}
                    type="email"
                    value={value}
                    onChange={(e) => {setValue(e.target.value)}}
                />
        </div>
        
        
    )
}

export function PasswordInput({label}: {label: string}) {
    const [value, setValue] = useState("")

    return (
        <div className="flex flex-col">
            <label id={value}>{label}</label>
                <input 
                    id={value}
                    className="bg-gray-200 p-2"
                    name={value}
                    type="password"
                    value={value}
                    onChange={(e) => {setValue(e.target.value)}}
                />
        </div>
        
        
    )
}