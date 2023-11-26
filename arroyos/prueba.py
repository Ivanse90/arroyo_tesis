import requests
from requests.exceptions import Timeout





auth_data = {
"keyPublic":"MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALy80H/oM09Nltj5nu2If3jlZ/baaE+Y3/vNHkUyxltRnHz7/BEJtuf/YGNdBe2/uloXjIoaVYpIbvA6IIxD8mMCAwEAAQ==",
"idProcess": "6baa0334-8ad2-41f7-a47d-2da271ab3b25",
"baseUrl":"https://stg-web.segurosbolivar.com/seguros-en-linea/soat-digital",
"data": {
    "name": "Simon",
    "lastName": "Bolivar Gomez",
    "numberPhone":"3153387996",
    "cityCode":"5002",
    "address":"Calle 116 # 67 - 21",
    "documentNumber": "1031123075",
    "documentType": "CC",
    "email": "correo@prueba.com",
    "habeasData": "true",
    "plate": "JXM742",
    "urlRedirect": "https://www.segurosbolivar.com/soat"
    }
}


url = 'https://87trkyimcf.execute-api.us-east-1.amazonaws.com/stage/tienda-seguridad/api/v1/autorizacion/sdk'


def peticion_sdk(base,data):
    """
    Input: url of endpoint,data about SDK,body, credencial AUTH
    Autor: Ivan Andres Serna 17-07-2023
    output: url encode  about access to  "Tienda Digital"
    the function "peticion_sdk" makes and get the url to get access to "tienda digital"
    this url will return decode
    """
    resp = requests.post(base, json=data, timeout=1)
    return resp

reqst = peticion_sdk(url,auth_data)

print(reqst.json())



