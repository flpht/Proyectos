function convertir() {
    const monto = document.getElementById('monto').value;
    const moneda = document.getElementById('moneda').value;
    fetch('/convertir', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ monto: monto, moneda: moneda })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('resultado').innerText = 'Error: ' + data.error;
        } else {
            let resultadoFormateado;
            // Aplicar formato específico dependiendo de la moneda
            if (moneda === 'usd') {
                // Conversión de USD a CLP (sin símbolo, sin decimales)
                resultadoFormateado = parseFloat(data.resultado).toLocaleString('es-CL', {
                    maximumFractionDigits: 0  // Asegura que no se muestren decimales
                });
            } else {
                // Conversión de CLP a USD (con símbolo, dos decimales)
                resultadoFormateado = parseFloat(data.resultado).toLocaleString('en-US', {
                    style: 'currency',
                    currency: 'USD',
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });
            }
            document.getElementById('resultado').innerText = 'Resultado: ' + resultadoFormateado;
        }
    });
}
