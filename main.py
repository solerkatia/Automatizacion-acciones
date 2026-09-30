import os
from dotenv import load_dotenv
from google import genai
import plotly.express as px
import yfinance as yf

# Cargar variables de entorno desde el archivo .env
load_dotenv()


def descargar_datos_financieros(tickers, period="1y"):
  """Descarga los datos históricos de cierre para los tickers indicados."""
  print("Descargando datos financieros...")
  datos = yf.download(tickers, period=period)
  precio = datos["Close"]
  return precio


def generar_graficos(precio):
  """Genera y guarda los gráficos interactivos con Plotly."""
  print("Generando visualizaciones...")

  # 1. Cotización histórica
  fig_cotizacion = px.line(
      precio,
      title="Cotización Histórica: Apple, Microsoft y Nvidia (12 meses)",
      labels={"value": "Precio (USD)", "Date": "Fecha"},
      template="plotly_dark",
  )
  fig_cotizacion.show()

  # 2. Rendimiento normalizado ($1000 invertidos)
  nom = (precio / precio.iloc[0]) * 1000
  fig_inversion = px.line(
      nom,
      title="Si invertías $1000, ¿cuánto tendrías hoy?",
      labels={"value": "Valor con $1000 (USD)", "Date": "Fecha"},
      template="plotly_dark",
  )
  fig_inversion.write_html("Inversion_de_1000_USD.html")
  print("Gráfico interactivo guardado como 'Inversion_de_1000_USD.html'")

  # 3. Precio promedio
  promedio = precio.mean()
  fig_barras = px.bar(
      promedio,
      title="Precio promedio: Apple, Nvidia y Microsoft",
      labels={"value": "Precio promedio (USD)", "index": "Empresa"},
      color=promedio.index,
      template="plotly_dark",
  )
  fig_barras.show()

  return nom


def generar_analisis_ia(precio):
  """Utiliza la API de Gemini para analizar los datos financieros."""
  print("Generando análisis con Gemini...")
  api_key = os.getenv("GEMINI_API_KEY")

  if not api_key:
    print(
        "Error: No se encontró la GEMINI_API_KEY en las variables de"
        " entorno."
    )
    return

  cliente = genai.Client(api_key=api_key)

  prompt = f"""
    Haz un análisis financiero del último año de las acciones de Apple, Microsoft y Nvidia.
    Considera tendencias generales y justifica las alzas o bajas relevantes basándote en el comportamiento de los datos:
    {precio.tail(30)}
    """

  respuesta = cliente.models.generate_content(
      model="gemini-3.8-flash",
      contents=prompt,
  )

  print("\n--- Análisis de la IA ---")
  print(respuesta.text)


if __name__ == "__main__":
  tickers_utilizados = ["AAPL", "NVDA", "MSFT"]

  # Ejecución del flujo
  precios_cierre = descargar_datos_financieros(tickers_utilizados)
  generar_graficos(precios_cierre)
  generar_analisis_ia(precios_cierre)