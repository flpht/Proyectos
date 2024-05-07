import bcchapi

def obtener_tasa_de_cambio():
    try:
        siete = bcchapi.Siete("elv.velasquez@duocuc.cl", "v-98Ee.P1998")
        tipo_de_cambio = siete.cuadro(
            series=["F073.TCO.PRE.Z.D"],
            nombres=["tipo_de_cambio_dolar"],
            desde="2024-01-01",  
            hasta="2024-12-01",
            frecuencia="D",
            observado={"tipo_de_cambio_dolar": "last"}
        )

        # Extrae el valor de la tasa de cambio
        tasa = tipo_de_cambio['tipo_de_cambio_dolar'].iloc[-1]
        print(f"Valor actual del dólar: {tasa} CLP")  # Muestra el valor actual del dólar
        return tasa
    except Exception as e:
        print("Error al obtener la tasa de cambio:", e)
        return None
    

def convertir_moneda(monto, moneda, tasa_usd_clp):
    if moneda.lower() == 'usd':
        resultado = monto * tasa_usd_clp
    elif moneda.lower() == 'clp':
        resultado = monto / tasa_usd_clp
    else:
        resultado = 'Moneda no válida'
    return resultado

def main():
    tasa_usd_clp = obtener_tasa_de_cambio()  # Obtiene la tasa de cambio una sola vez al inicio
    if tasa_usd_clp is None:
        return  # Finaliza el programa si no se puede obtener la tasa de cambio

    while True:
        try:
            monto = float(input("Ingrese el monto a convertir: "))
            moneda = input("Ingrese la moneda de origen (USD o CLP): ")

            if moneda.lower() not in ['usd', 'clp']:
                print("Moneda no válida. Por favor, ingrese 'USD' o 'CLP'.")
                continue

            resultado = convertir_moneda(monto, moneda, tasa_usd_clp)
            if isinstance(resultado, str):
                print(resultado)

            else:
                # Aquí formateamos el resultado como moneda con separadores de miles
                resultado_formateado = "{:,.0f}".format(resultado).replace(",", ".")
                print(f"El monto convertido es: ${resultado_formateado} ")
            continuar = input("¿Desea realizar otra conversión? (s/n): ")
            if continuar.lower() != 's':
                break
        except ValueError:
            print("Por favor, ingrese un número válido.")

if __name__ == "__main__":
    main()
