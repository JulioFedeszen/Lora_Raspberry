from utils.logger import Logger

import RPi.GPIO as GPIO
from infra.db import Database
from services.processa_dados import ProcessaDados
class Main:
    
    def __init__(self):
        self._processa_dados = ProcessaDados()
        
    
    def run(self):
        self._processa_dados.processa_dados()


            
if __name__ == "__main__":
    Logger.info("Raspberry Pi pronto para receber via LoRa UART")
    
    try:
        Main().run()
    except KeyboardInterrupt:
        Logger.warn("Encerrando o programa...")
    finally:
        GPIO.cleanup()
        Database().close()
        