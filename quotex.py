import requests
import pandas as pd
import time
import logging

# Configurações do sistema de logs
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configurações do Bot
API_KEY = "YOUR_API_KEY_HERE"  # Substituir pelo valor real
API_SECRET = "YOUR_API_SECRET_HERE"  # Substituir pelo valor real
BROKER_NAME = "alpaca"
BASE_URL = "https://paper-api.alpaca.markets"
SYMBOL = "AAPL"
FETCH_INTERVAL = 60  # Tempo entre ciclos de negociação (em segundos)
MAX_POSITION_SIZE = 100  # Tamanho máximo da posição (em ações)
MAX_DAILY_LOSS = 500  # Perda diária máxima permitida (em USD)


class Broker:
    def __init__(self, api_key, api_secret, broker_name):
        self.api_key = api_key
        self.api_secret = api_secret
        self.broker_name = broker_name
        self.base_url = BASE_URL
        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret,
        }

    def get_positions(self):
        """Obtém posições abertas no broker."""
        url = f"{self.base_url}/v2/positions"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                positions = response.json()
                logging.info(f"Posições abertas: {positions}")
                return positions
            else:
                logging.error(f"Erro ao obter posições: {response.json()}")
                return []
        except Exception as e:
            logging.error(f"Erro na consulta de posições: {str(e)}")
            return []

    def place_order(self, symbol, side, quantity):
        """Envia uma ordem de compra ou venda para o broker."""
        positions = self.get_positions()
        for position in positions:
            if position['symbol'] == symbol:
                logging.info(f"Já existe posição aberta em {symbol}, ignorando ordem.")
                return  # Ignorar ordem se já houver posição aberta

        url = f"{self.base_url}/v2/orders"
        payload = {
            "symbol": symbol,
            "qty": quantity,
            "side": side.lower(),
            "type": "market",
            "time_in_force": "gtc",
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code == 200:
                logging.info(f"Ordem enviada: {response.json()}")
            else:
                logging.error(f"Erro ao enviar ordem: {response.json()}")
        except Exception as e:
            logging.error(f"Erro ao executar ordem: {str(e)}")


class RiskManager:
    def __init__(self, max_position_size, max_daily_loss):
        """Inicializa o gerenciador de risco."""
        self.max_position_size = max_position_size
        self.max_daily_loss = max_daily_loss
        self.current_loss = 0

    def check_risk(self, signal, symbol, broker):
        """Verifica se a negociação é permitida dentro dos limites de risco."""
        positions = broker.get_positions()
        for position in positions:
            if position['symbol'] == symbol:
                position_size = int(position['qty'])
                if position_size >= self.max_position_size:
                    logging.warning(f"Tamanho máximo da posição atingido para {symbol}.")
                    return False

        if self.current_loss >= self.max_daily_loss:
            logging.warning("Limite de perda diária atingido.")
            return False

        return True


def fetch_market_data(symbol):
    """Busca dados de mercado para o símbolo fornecido."""
    url = f"{BASE_URL}/v2/stocks/{symbol}/quote"
    headers = {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": API_SECRET,
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {
                "symbol": symbol,
                "price": data["last"]["price"],
                "ask": data["askprice"],
                "bid": data["bidprice"],
            }
        else:
            logging.error(f"Erro ao buscar dados de mercado: {response.json()}")
            return None
    except Exception as e:
        logging.error(f"Erro na coleta de dados de mercado: {str(e)}")
        return None


def calculate_moving_average(data, period):
    """Calcula a média móvel simples (SMA)."""
    return data['close'].rolling(window=period).mean()


def generate_signal(data):
    """Gera sinais de negociação com base em médias móveis."""
    if 'close' not in data.columns:
        raise ValueError("Os dados de mercado devem conter uma coluna 'close'.")

    data['SMA_10'] = calculate_moving_average(data, 10)
    data['SMA_50'] = calculate_moving_average(data, 50)

    if data['SMA_10'].iloc[-1] > data['SMA_50'].iloc[-1]:
        return "BUY"
    elif data['SMA_10'].iloc[-1] < data['SMA_50'].iloc[-1]:
        return "SELL"
    else:
        return "HOLD"


def main():
    # Inicializar o broker
    broker = Broker(api_key=API_KEY, api_secret=API_SECRET, broker_name=BROKER_NAME)

    # Inicializar o gerenciador de risco
    risk_manager = RiskManager(max_position_size=MAX_POSITION_SIZE, max_daily_loss=MAX_DAILY_LOSS)

    # Inicializar histórico de preços
    price_history = pd.DataFrame(columns=["close"])

    # Loop de negociação
    while True:
        try:
            # Passo 1: Buscar dados de mercado
            market_data = fetch_market_data(SYMBOL)
            if market_data is None:
                time.sleep(FETCH_INTERVAL)
                continue

            # Atualizar o histórico de preços
            price_history = price_history.append({"close": market_data["price"]}, ignore_index=True)

            # Garantir que há dados suficientes para calcular indicadores
            if len(price_history) >= 50:
                # Passo 2: Gerar sinal de negociação
                signal = generate_signal(price_history)

                # Passo 3: Verificar risco e executar ordens
                if risk_manager.check_risk(signal, SYMBOL, broker):
                    if signal == "BUY":
                        broker.place_order(SYMBOL, "BUY", quantity=10)
                    elif signal == "SELL":
                        broker.place_order(SYMBOL, "SELL", quantity=10)

                # Log do sinal gerado
                logging.info(f"Sinal gerado: {signal} para o símbolo {SYMBOL}")

            # Esperar antes do próximo ciclo
            time.sleep(FETCH_INTERVAL)

        except Exception as e:
            logging.error(f"Erro no loop principal: {str(e)}")
            time.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    main()
