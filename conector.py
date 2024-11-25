import requests

class Conector():

    def __init__(self):
        self.ESP_IP = "http://192.168.138.64"

    def abrir_cancela(self):
        try:
            response = requests.get(f"{self.ESP_IP}/abrir")
            if response.status_code == 200:
                print("Comando enviado: Abrir cancela")
                print("Resposta do ESP:", response.text)
            else:
                print("Erro ao enviar comando. Código:", response.status_code)
        except Exception as e:
            print("Erro na comunicação com o ESP:", e)

    def fechar_cancela(self):
        while True:
            try:
                response = requests.get(f"{self.ESP_IP}/fechar")
                if response.status_code == 200:
                    print("Comando enviado: Fechar cancela")
                    print("Resposta do ESP:", response.text)
                    break
                else:
                    print("Erro ao enviar comando. Código:", response.status_code)
            except Exception as e:
                print("Erro na comunicação com o ESP:", e)

    def fechar_cancela_manualmente(self):
        while True:
            try:
                response = requests.get(f"{self.ESP_IP}/fechar_manualmente")
                if response.status_code == 200:
                    print("Comando enviado: Fechar cancela manualmente")
                    print("Resposta do ESP:", response.text)
                    break
                else:
                    print("Erro ao enviar comando. Código:", response.status_code)
            except Exception as e:
                print("Erro na comunicação com o ESP:", e)

