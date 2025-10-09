"use client"

import { TextInput } from "@/components/forms"

export default function Login() {
    
    return (
        <div className="flex justify-center items-center h-full">
            <div className="md:border md:rounded-xl w-[60%] h-[60%] p-4">
                <form className="flex flex-col gap-y-8 items-center">
                    <TextInput label="Email"></TextInput>     
                    <TextInput label="Password"></TextInput>
                    <button className="bg-blue-500 w-1/3 h-10 rounded-xl">Submit</button>               
                </form>
                <a href="/create_account">I don&apos;t have an account</a>
            </div>
        </div>
       
        
    )
}