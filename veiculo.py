
class GerenciadorVeiculos:

    def __init__(self):
        self.placas_precadastradas = {
        'ABC1D23': ['Moto', 'Honda', '2017', 'Vermelho', 'Gabriel Brito'],
        'EFG4H56': ['Moto', 'Honda', '2015', 'Preto', 'Ednaldo Pereira'],
        'IJK7891': ['Moto', 'Yamaha', '2022', 'Azul Escuro', 'Aureliano Buendía'],
        'LMN7258': ['Carro', 'Chevrolet', '2017', 'Cinza', 'Harrison Ford'],
        'ABC4F78': ['Carro', 'Fiat', '2007', 'Preto', 'Jessé Lineu Silva'],
        #'FGV8G41': ['Carro', 'Honda', '2014', 'Preto', 'Jeronimo Einstein'],
        'GPT1W45': ['Carro', 'Peogeut', '2019', 'Azul', 'Esdras da Silva Sauro']
        }


    def cadastrar(self, placa, lista_de_atributos):
        self.placas_precadastradas[placa] = lista_de_atributos
        print(self.placas_precadastradas[placa])
        print(self.placas_precadastradas)


    def verificar_cadastrados(self, detected_texts):
        try:
            _ = self.placas_precadastradas[detected_texts]
            return self.placas_precadastradas[detected_texts]
        except:
             return []
