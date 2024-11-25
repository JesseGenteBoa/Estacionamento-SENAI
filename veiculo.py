
class Veiculo:

    def __init__(self):
        self.placas_precadastradas = {
        'ABC1D23': ['Moto', 'Honda', '2017', 'Vermelho', 'Gabriel Brito'],
        'EFG4H56': ['Moto', 'Honda', '2015', 'Preto', 'Ednaldo Pereira'],
        'IJK7891': ['Moto', 'Yamaha', '2022', 'Azul Escuro', 'Pedro Aureliano Buendía'],
        'LMN7258': ['Carro', 'Chevrolet', '2017', 'Cinza', 'Harrison Ford'],
        'ABC4F78': ['Carro', 'Fiat', '2007', 'Preto', 'Jessé Ramos'],
        'FGV8G41': ['Carro', 'Honda', '2014', 'Preto', 'Jeronimo Einstein'],
        'GPT1W45': ['Carro', 'Peogeut', '2019', 'Azul', 'Esdras da Silva Sauro']
        }


    def cadastrar(self, placa, lista_de_atributos):
        self.placas_precadastradas[placa] = lista_de_atributos
        

    def imprimir_cadastrados(self, placa):    
        print(self.placas_precadastradas[placa])
        #return self.placas_precadastradas[placa]


    def verificar_cadastrados(self, detected_texts):
        try:
            _ = self.placas_precadastradas[detected_texts]
            return True
        except:
             return False
