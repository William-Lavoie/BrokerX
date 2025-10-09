"use client"

import { useState } from "react"

type TextInputProps = {
  label: string;
  id?: string;
  name?: string;
  type?: string;
  handler?: (e: React.ChangeEvent<HTMLInputElement>) => void;
};

export function TextInput({ label, id, name, type = "text", handler }: TextInputProps) {    
    const [value, setValue] = useState("")

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setValue(e.target.value);
        if (handler) {
            handler(e);
        }
    };
    return (
        <div className="flex flex-col">
            <label htmlFor={id ?? label}>{label}</label>
                <input 
                    id={id ?? label}
                    className="bg-gray-200 w-full min-w-[150px] p-2 appearance-none"
                    name={name ?? label}
                    type={type ?? "text"}
                    value={value}
                    onChange={handleChange}
                />
        </div>
    )
}