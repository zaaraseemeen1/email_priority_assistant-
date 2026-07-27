// three inputs 
// classify button
// onclick of classify fetch with three values sent as JSON to provided link
import {useState} from "react";

function EmailForm() {

    // piece of state that represents the email the user wants classified 
    const [email, setEmail] = useState(
        {
            sender: "",
            subject: "",
            body: ""
        }
    );

    // setting aside a piece of state to hold the result of the email (which will be just a string)
    const [result, setResult] = useState("")

    // async function means this function is allowed to await things inside of it
    const submitEmail = async () => {
        const response = await fetch(`http://localhost:5000/classify`, {
            method: "POST", // here's some data I want you to process/create something from
            headers: { "Content-Type": "application/json" }, // tells the backend to parse the text as JSON
            body: JSON.stringify(email) // converts JS object to text (can only be sent over the network as text)
        });
        
        const classification = await response.json(); // network requests take time
        setResult(classification.result); // using key to pull out value

    }

   return (
    <div id = "email_form">
        <form onSubmit = {(e) => {e.preventDefault(); submitEmail()}}>
            <label htmlFor = "sender">Sender</label> 
            <input 
                type ="text" 
                placeholder = "e.g. john.doe@company.com@domain" 
                value = {email.sender} 
                onChange={(e) => setEmail({ ...email, sender: e.target.value })}
                id ="sender">
            </input> 

            <label htmlFor = "subject">Subject</label> 
            <input type ="text" 
                placeholder = "e.g. Quarterly Report – Q3 Review" 
                value = {email.subject} 
                onChange={(e) => setEmail({ ...email, subject: e.target.value })}
                id ="subject">
            </input> 

            <label htmlFor = "body">Body</label> 
            <input type ="text"
                placeholder = "Paste the email content here..." 
                value = {email.body} 
                onChange={(e) => setEmail({ ...email, body: e.target.value })}
                id ="body">
            </input>   

            <button>Classify</button>
        </form>
    </div>
   );
}