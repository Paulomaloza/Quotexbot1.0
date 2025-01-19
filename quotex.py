import time
import numpy as np
import talib
from quotexapi.stable_api import Quotex


class QuotexBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.bot = Quotex(email, password)
        self.token = None
        self.token_expiration = None
    
    def conectar(self):
        """Conecta ao Quotex e autentica."""
        response = self.bot.login(self.email, self.password)
        
        if response["status"] == "success":
            self.token = response["token"]
            self.token_expiration = time.time() + response["expires_in"]
            print(f"✅ Login bem-sucedido! Token: {self.token}")
            return True
        else:
            self.tratar_erro(response)
            return False
    
    def is_token_valid(self):
        """Verifica se o token ainda é válido."""
        if self.token and self.token_expiration > time.time():
            return True
        return False
    
    def desconectar(self):
        """Desconecta do Quotex."""
        response = self.bot.logout()
        
        if response["status"] == "success":
            self.token = None
            self.token_expiration = None
            print(f"🔌 Logout bem-sucedido: {response['message']}")
        else:
            self.tratar_erro(response)
    
    def tratar_erro(self, response):
        """Trata as respostas de erro."""
        if response["status"] == "error":
            error_code = response.get("error_code", "UNKNOWN_ERROR")
            message = response.get("message", "Erro desconhecido")
            print(f"❌ Erro: {message} (Código: {error_code})")
    
    def get_saldo(self):
        """Retorna o saldo atual."""
        if not self.is_token_valid():
            print("⚠️ Token expirado. Reconectando...")
            self.conectar()
        
        response = self.bot.get_balance()
        
        if response["status"] == "success":
            saldo = response["balance"]
            moeda = response["currency"]
            print(f"💰 Saldo atual: {saldo:.2f} {moeda}")
            return saldo
        else:
            self.tratar_erro(response)
            return None
    
    def get_detalhes_conta(self):
        """Obtém os detalhes da conta do usuário."""
        if not self.is_token_valid():
            print("⚠️ Token expirado. Reconectando...")
            self.conectar()
        
        response = self.bot.get_account_details()
        
        if response["status"] == "success":
            conta = response["account"]
            print(f"👤 Detalhes da Conta:")
            print(f"  ID: {conta['id']}")
            print(f"  Nome: {conta['name']}")
            print(f"  E-mail: {conta['email']}")
            print(f"  Tipo de Conta: {conta['account_type']}")
            print(f"  Saldo: {conta['balance']:.2f} {conta['currency']}")
        else:
            self.tratar_erro(response)
    
    def realizar_negociacao(self, ativo, direcao, valor, tempo_expiracao):
        """
        Realiza uma negociação.
        :param ativo: Par de moedas ou ativo (exemplo: 'EUR/USD').
        :param direcao: 'CALL' (subida) ou 'PUT' (queda).
        :param valor: Valor investido.
        :param tempo_expiracao: Duração da negociação (em minutos ou tempo exato).
        """
        if not self.is_token_valid():
            print("⚠️ Token expirado. Reconectando...")
            self.conectar()
        
        print(f"🚀 Negociando: Ativo={ativo}, Direção={direcao}, Valor=${valor}, Tempo={tempo_expiracao}")
        resultado = self.bot.place_trade(
            asset=ativo,
            direction=direcao,
            amount=valor,
            expiration_time=tempo_expiracao
        )
        
        if resultado["status"] == "success":
            print(f"✅ Negociação realizada com sucesso!")
            print(f"  ID da negociação: {resultado['trade_id']}")
            print(f"  Ativo: {resultado['asset']}")
            print(f"  Direção: {resultado['direction']}")
            print(f"  Valor investido: ${resultado['amount']}")
            print(f"  Tempo de expiração: {resultado['expiration_time']}")
            print(f"  Retorno potencial: ${resultado['potential_payout']}")
        else:
            self.tratar_erro(resultado)
        return resultado
    
    def obter_lista_ativos(self):
        """Retorna a lista de ativos disponíveis."""
        if not self.is_token_valid():
            print("⚠️ Token expirado. Reconectando...")
            self.conectar()
        
        response = self.bot.get_asset_list()
        
        if response["status"] == "success" and "assets" in response:
            assets = response["assets"]
            print("📊 Lista de Ativos Disponíveis:")
            for asset in assets:
                print(f"  Símbolo: {asset['symbol']}")
                print(f"  Nome: {asset['name']}")
                print(f"  Payout: {asset['payout']}%")
        else:
            self.tratar_erro(response)
        
        return response

    def obter_detalhes_ativo(self, ativo):
        """Retorna os detalhes de um ativo específico."""
        if not self.is_token_valid():
            print("⚠️ Token expirado. Reconectando...")
            self.conectar()
        
        response = self.bot.get_asset_details(ativo)
        
        if response["status"] == "success":
            asset = response["asset"]
            print(f"📈 Detalhes do Ativo: {asset['name']} ({asset['symbol']})")
            print(f"  Payout: {asset['payout']}%")
            print(f"  Status do Mercado: {asset['market_status']}")
            print(f"  Volatilidade: {asset['volatility']}")
        else:
            self.tratar_erro(response)
        
        return response


# Funções auxiliares para cálculo dos indicadores (RSI e MACD)
def calcular_indicadores(candles):
    closes = [candle['close'] for candle in candles]
    
    # Calculando RSI e MACD
    rsi = talib.RSI(np.array(closes), timeperiod=14)
    macd, macdsignal, _ = talib.MACD(np.array(closes), fastperiod=12, slowperiod=26, signalperiod=9)
    
    return rsi, macd, macdsignal

def detectar_suporte_resistencia(candles):
    lows = [candle['low'] for candle in candles]
    highs = [candle['high'] for candle in candles]
    
    support = min(lows)
    resistance = max(highs)
    
    return support, resistance


# Configurações de Login
EMAIL = "seu_email@example.com"
PASSWORD = "sua_senha"

if __name__ == "__main__":
    bot = QuotexBot(EMAIL, PASSWORD)
    
    # Conectar ao Quotex
    if bot.conectar():
        ativo = "EUR/USD"
        
        # Obter candles para análise
        candles = bot.bot.get_candles(ativo, 60, 100)
        
        # Calcular RSI e MACD
        rsi, macd, macdsignal = calcular_indicadores(candles)
        
        # Detectar suporte e resistência
        support, resistance = detectar_suporte_resistencia(candles)
        
        # Verificando condições de compra
        if rsi[-1] < 30 and macd[-1] > macdsignal[-1] and candles[-1]['close'] <= support:
            bot.realizar_negociacao(ativo, "CALL", 100, "1m")
        
        # Verificando condições de venda
        elif rsi[-1] > 70 and macd[-1] < macdsignal[-1] and candles[-1]['close'] >= resistance:
            bot.realizar_negociacao(ativo, "PUT", 100, "1m")
        
        # Desconectar após a operação
        bot.desconectar()
