import RPi.GPIO as GPIO
import time
import serial
import json
from utils.logger import Logger

class Lora:
    def __init__(self, serial_port="/dev/serial0", baudrate=9600, timeout=1,
                 m0_pin=23, m1_pin=24, aux_pin=18):
        self._m0_pin = m0_pin
        self._m1_pin = m1_pin
        self._aux_pin = aux_pin
        self._coletor_id = "96741762-1d52-4558-8d95-232b85d5f6aa"
        self._log = Logger()
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._m0_pin, GPIO.OUT)
        GPIO.setup(self._m1_pin, GPIO.OUT)
        GPIO.setup(self._aux_pin, GPIO.IN)

        GPIO.output(self._m0_pin, GPIO.LOW)
        GPIO.output(self._m1_pin, GPIO.LOW)

        self._lora = serial.Serial(serial_port, baudrate, timeout=timeout)

    def wait_for_module_ready(self):
        while GPIO.input(self._aux_pin) == 0:
            time.sleep(0.01)

    def read_message(self):
        self.wait_for_module_ready()
        if self._lora.in_waiting:
            msg = self._lora.readline().decode('utf-8', errors='ignore').strip()
            return msg
        return None
        
    def write(self, data):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("O dado enviado deve ser do tipo bytes.")
        try:
            self._log.info(f"Preparando para enviar: {data}")
            self.wait_for_module_ready()
            self._lora.write(data)
            self._log.info("Dados enviados com sucesso.")
        except Exception as e:
            self._log.error(f"Erro ao enviar dados: {e}")
                
    def send_ok(self):
        comando = {
            "coletor_id": self._coletor_id,
            "assunto": "resposta",
            "acao": "ok"
        }
        self.write((json.dumps(comando) + "\n").encode('utf-8'))

    def send_nok(self):
        comando = {
            "coletor_id": self._coletor_id,
            "assunto": "resposta",
            "acao": "nok"
        }
        self.write((json.dumps(comando) + "\n").encode('utf-8'))

    def send_turn_on_irrigation(self, no_id):
        comando = {
            "coletor_id": self._coletor_id,
            "assunto": "irrigacao",
            "acao": "irrigar",
            "no_id": no_id
        }
        self.write((json.dumps(comando) + "\n").encode('utf-8'))

    def send_turn_off_irrigation(self, no_id):
        comando = {
            "coletor_id": self._coletor_id,
            "assunto": "irrigacao",
            "acao": "parar",
            "no_id": no_id
        }
        self.write((json.dumps(comando) + "\n").encode('utf-8'))