"""
Projeto 2
Analise de uma missao lunar usando propulsao elétrica transferencia orbital e umk propelente 
hipergolico green para o pouso

"""

import numpy as np

class PropEletrica:
    
    def __init__(self, params, **kwargs):
        self.params = params  # Vai ser um dicionario com os parametros
        
        
        # Obtendo valores dos parâmetros
        self.pe = self.params.get("pe", 0)
        self.p_jet = self.params.get("p_jet", 0)
        self.aceralaracao = self.params.get("aceralaracao", 0)
        self.g0 = self.params.get("g0", 9.81)  # Gravidade padrão, m/s²
        self.isp = self.params.get("isp", 0)
        self.empuxo = self.params.get("empuxo", 0)
        self.v = self.params.get("v", 0)
        self.tp = self.params.get("tp", 0)
        self.nt = self.params.get("nt", 0)
        self.delta_v = params.get("delta_v", 0)
        self.alpha = params.get("alpha", 0)
        
        # Massas
        self.m0 = self.params.get("m0", 0)
        self.m_prop = self.params.get("m_prop", 0)  # Massa do propelente
        self.m_pp = self.params.get("m_pp", 0)  # Massa do sistema propulsivo
        self.m_pl = self.params.get("m_pl", 0)  # Massa do pay load
    
    
        # Painel
        self.efic_solar =  self.params.get("efic_solar", 0)
        self.i_sol = self.params.get("i_sol", 0)
        self.sigma_painel = self.params.get("sigma_painel", 0)   
    
    def calcula_massas(self):
        # Calculando a massa do sistema propulsivo se não for fornecida
           
        
        if self.m_prop == 0:  
            self.m_prop_ponto = self.empuxo / (self.isp * self.g0)
            if self.tp != 0:
                self.m_prop = self.m_prop_ponto * self.tp
                print(f'Massa do sistema propulsivo: {self.m_prop} kg')

        if self.m_pp == 0 and self.alpha != 0:
            pe = self.calcula_pot_eletrica()
            self.m_pp = pe / self.alpha if self.alpha != 0 else 0

        elif self.m0 != 0:
            self.m_pp = self.m0 - self.m_prop - self.m_pl
        
        if self.m0 == 0:
            # Calculando as massas
            self.m0 = self.m_prop + self.m_pp + self.m_pl  # Massa total
        return self.m0
    
    def calcula_pot_eletrica(self):
        self.calcula_v()
        # Calculando a potência específica se não for fornecida
        if self.pe == 0 and self.nt != 0:
            self.pe =(0.5 * self.m_prop_ponto * (self.v ** 2)) / self.nt 
        
        return self.pe
    
    def calcula_delta_v(self):
        self.delta_v = self.g0 * self.isp * np.log(self.m0 / (self.m0 - self.m_prop))
        return self.delta_v
    
    def aceleracao_veiculo(self):
        self.aceralaracao = self.delta_v / self.tp # nao sei se esta certo
        return self.aceralaracao
    
    def calcula_pot_cinetica(self):
        # Calculando a potência cinética do jato
        self.p_jet = (0.5 * self.g0 * self.isp) * self.empuxo
        return self.p_jet
        
    def calcula_v(self):
        self.v = self.isp * self.g0
        return self.v
    
    def calcula_relacoes_fundamentais(self):
        
        # Definindo potência elétrica
        self.pe = self.calcula_pot_eletrica() if self.pe == 0 else self.pe
               
        # Calculando a potência específica
        self.alpha = self.pe / self.m_pp if self.m_pp != 0 else 0
        
        # calculando a potência cinética do jato
        self.p_jet = self.calcula_pot_cinetica() if self.p_jet == 0 else self.p_jet
        
        # Calculando a eficiência do sistema
        if self.pe != 0:
            self.nt = (self.empuxo * self.isp * self.g0) / (2 * self.pe)
        
        
        # Velocidade característica (não física, apenas agrupamento de parâmetros)
        if self.alpha != 0 and self.nt != 0:
            self.vc = np.sqrt(2 * self.alpha * self.nt * self.tp)
        
        else:
            self.vc = 0
        
        self.delta_v = self.calcula_delta_v() if self.delta_v == 0 else self.delta_v
        self.aceralaracao = self.aceleracao_veiculo() if self.aceralaracao == 0 else self.aceralaracao
        
        
        return {
            "m_prop_ponto": self.m_prop_ponto,
            "m_prop": self.m_prop,
            "m_pp": self.m_pp,
            "massa_total":self.m0,
            "P_eletrica": self.pe,
            "P_jet":self.p_jet,
            "delta_v": self.delta_v,
            "a": self.aceralaracao,
        }
    
    def calcula_parametros_painel(self):
        self.area_painel = self.pe / (self.efic_solar * self.i_sol)
        self.m_painel = self.area_painel * self.sigma_painel 
        
        return {
            "Area painel": self.area_painel,
            "massa painel": self.m_painel,

        }
    
        
    
    
    

"""
Perguntas principais:
    - Calcular a massa de combustível para transferir o veículo de uma órbita GTO para uma órbita lunar.
    - Estimar a potência necessária e as massa inertes dos componentes
    - Considerando que a energia que alimenta os propulsores vem dos painéis solares. Estime sua massa e dimensões.
    - Avaliar um sistema de propulsão hipergólico green para o pouso
"""

params = {
    "delta_v": 4000, # km/s
    "m_pl": 8000, # SMART-1 (Small Missions for Advanced Research in Technology)
    "propelente": "xenonio", # sem unidade
    "empuxo": 70 * (10**-3), # Newtons 
    "isp": 2000, # segundos
    "tp": 26 * (60 * 60 * 24 * 30), # segundos - 4 semanas
    "nt":0.6,
    "alpha": 80,
    "efic_solar": 0.15,
    "i_sol": 1000 ,
    "sigma_painel": 6

}

# Instanciando e executando a classe
prop_el = PropEletrica(params)
massa_total = prop_el.calcula_massas()
relacoes_fundamentais = prop_el.calcula_relacoes_fundamentais()
parametros_painel = prop_el.calcula_parametros_painel()

print("################################ Relacoes Fundamentais: ################################")
for chave, valor in relacoes_fundamentais.items():
    print(f'{chave}: {valor}')

print("########################################################################################")


print("################################ Painel: ################################")
for chave, valor in parametros_painel.items():
    print(f'{chave}: {valor}')

print("########################################################################################")



