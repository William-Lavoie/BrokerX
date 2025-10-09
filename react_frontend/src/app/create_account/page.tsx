"use client"

import { TextInput } from "@/components/forms"
import { useState } from "react"

export default function Login() {
    
    const [email_error, setEmailError] = useState("");
    const [password_error, setPasswordError] = useState("");
    const [password_confirm_error, setConfirmedPasswordError] = useState("");

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

        if (password && !password.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")) {
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

    return (
        <div className="flex justify-center items-center h-full">
            <div className="md:border md:rounded-xl w-[70%] p-4">
                <form className="flex flex-col gap-y-8 items-center">
                    <div className="sm:flex sm:flex-row sm:gap-x-6">
                        <TextInput label="First Name"></TextInput>     
                        <TextInput label="Last Name"></TextInput>   
                    </div>
                    
                    <div className="sm:flex sm:flex-row sm:gap-x-6">
                        <TextInput label="Email address" id="email-input" type="email" handler={emailMatch}></TextInput>  
                        <div>
                            <TextInput label="Confirm Email" id="confirm-email-input" type="email" handler={emailMatch}></TextInput>
                            <span className="text-red-500">{email_error}</span>       
                        </div>   
                    </div>

                    <div className="sm:flex sm:flex-row sm:gap-x-6">
                        <TextInput label="Phone Number" type="tel"></TextInput>     
                        <TextInput label="Date of Birth" type="date"></TextInput>  {/* TODO: fix width */}
                    </div>

                    <div className="sm:flex sm:flex-row sm:gap-x-6">
                        <TextInput label="Address" type="text"></TextInput> 
                        <div className="w-50">
                            <label id="communication-method">Preferred communication method</label>
                            <select id="communication-method" className="bg-gray-200 w-full min-w-[150px] p-2 appearance-none">
                                <option>Email</option>
                                <option>SMS</option>
                            </select> 
                        </div>
                        
                    </div>

                    <div className="sm:flex sm:flex-row sm:gap-x-6">
                        <div>
                            <TextInput label="Password" id="password-input" type="password" handler={validatePasswords}></TextInput>
                            <span className="text-red-500">{password_error}</span>       
                        </div>
                      
                        <div>
                            <TextInput label="Confirm Password" id="confirm-password-input" type="password" handler={validatePasswords}></TextInput> 
                            <span className="text-red-500">{password_confirm_error}</span>       
                        </div>    
                    </div>
                     
                    <button className="bg-blue-500 w-1/3 h-10 rounded-xl">Submit</button>               
                </form>
                <a href="/create_account">I don&apos;t have an account</a>
            </div>
        </div>
       
        
    )
}