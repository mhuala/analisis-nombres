import requests
import pandas as pd

REGISTRO_CIVIL_URL = "https://codigo.registrocivil.cl/api/estnombre/ltRanking/"
l = [] 
headers = {"Content-Type": "application/json",
           "Accept": "application/json, text/plain",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "es-ES,es;q=0.9",
           "Content-Length": "37",
           "Origin": "https: //estadisticas.sed.srcei.cl",
           "Referer": "https: //estadisticas.sed.srcei.cl",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0"}
# Listas de opciones
years_list = [str(x) for x in range(2010, 2022)]
months_list = [str(x) for x in range(1, 13)]
sex_list = ["F", "M"]

for year in years_list:
    for month in months_list:
        for sex in sex_list:
            # Payload variable
            payload = {"year": year, "sex": sex, "month": month}
            # Envio de petición
            response = requests.post(REGISTRO_CIVIL_URL, headers=headers, json=payload)
            # Transformación de respuesta
            resp_dict = response.json()
            # Iteración sobre respuesta
            for data_entry in resp_dict:
                # Añadir a la lista
                l.append(
                    {
                        "nombre": data_entry["nombre"],
                        "cantidad": data_entry["cantidad"],
                        "year": year,
                        "sex": sex,
                        "month": month,
                    }
                )
                
df = pd.DataFrame.from_records(l) 
df.to_csv(f"Nombres {str(years_list[0])}-{str(years_list[-1])}.csv")