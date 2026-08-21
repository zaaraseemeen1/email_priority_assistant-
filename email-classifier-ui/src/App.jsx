import EmailForm from "./components/EmailForm"
import ResultDisplay from "./components/ResultDisplay"
import {useState} from "react";

function App() {

    // result lives here since both pieces of state need access to it
    const [result, setResult] = useState(null)

    return (
        <div>
            <EmailForm setResult = {setResult}/>
            <ResultDisplay result = {result}/>
        </div>
    );

} 
export default App;