document.getElementById("predictionForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        studytime: parseInt(document.getElementById("studytime").value),
        failures: parseInt(document.getElementById("failures").value),
        absences: parseInt(document.getElementById("absences").value),
        G1: parseInt(document.getElementById("G1").value),
        G2: parseInt(document.getElementById("G2").value)
    };

    const response = await fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    document.getElementById("result").innerHTML = `
        <h2>Prediction: ${result.prediction}</h2>
        <p>${result.advice}</p>
    `;
});