import paho.mqtt.client as mqtt
import time

# Configurações do MQTT
broker = "127.0.0.1"  # Mesmo broker do publicador
port = 1883
topic = "dev9840ss"   # Mesmo tópico do publicador

# Callback quando uma mensagem é recebida
def on_message(client, userdata, msg):
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{timestamp}] Valor recebido: {msg.payload.decode()}")

# Configurar cliente MQTT
subscriber = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "ouvinte_angulo")
subscriber.on_message = on_message

try:
    print(f"Conectando ao broker {broker}...")
    subscriber.connect(broker, port)
    subscriber.subscribe(topic)
    print(f"Ouvindo tópico: {topic}")
    print("Aguardando valores (Ctrl+C para parar)...")
    subscriber.loop_forever()  # Mantém a conexão ativa

except KeyboardInterrupt:
    print("\nEncerrando ouvinte...")
    subscriber.disconnect()
except Exception as e:
    print(f"Erro: {e}")