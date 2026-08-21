const colorMapper = {
    Important: "#1B7F37",
    Normal: "#6B7280",
    Noise: "#C1272D"
}

function ResultDisplay(prop) {

    if (prop.result == null) {
        return null;
    } else {
        return (
            <h1 style = {{color: colorMapper[prop.result]}}>{prop.result}</h1>
        );
    }
}

export default ResultDisplay;