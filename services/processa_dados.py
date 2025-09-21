import time
import json
from utils.logger import Logger

from repositories.acoes_db import AcoesDB
from services.lora import Lora
from services.valida_dados import ValidaDados
from services.define_irrigacao import DefineIrrigacao

class ProcessaDados:
    def __init__(self, coletor_id='96741762-1d52-4558-8d95-232b85d5f6aa'):
        self._acoes_db = AcoesDB()
        self._lora = Lora()
        self._coletor_id = coletor_id
        self._valida = ValidaDados()
        self._log = Logger()
        self._define_irrigacao = DefineIrrigacao()
        
    
    def _insere_dados(self, temp, umi_solo, umi_ar, chuva, no_id):
       
            self._acoes_db.inserir_dados_coletados(
                coletor_id=self._coletor_id,
                no_id=no_id,
                temperatura=temp,
                umidade_solo=umi_solo,
                umidade_ar=umi_ar,
                chuva=chuva
            )
            self._log.info("Dados inseridos com sucesso!")
            self._lora.send_ok() 
            
    def processa_dados(self):
        """Processa os dados recebidos via LoRa
        Lê mensagens do módulo LoRa, valida e insere os dados no banco de dados.
        Também verifica se deve iniciar a irrigação com base nos dados recebidos.
        Envia respostas de confirmação (OK/NOK) de volta ao nó.
        Executa em loop contínuo, aguardando novas mensagens.
        
        Quando assunto é 'coleta', espera os campos:
        - no (identificador do nó)
        - dados (dicionário com os dados coletados)
        Exemplo de mensagem esperada:
        {
        "no": "3b8073c0-5f89-4a8f-b554-6af32a60cb2d",
        "assunto": "coleta",
        "dados": {
            "temperatura": 26.4,
            "umidade_solo": 58,
            "umidade_ar": 72,
            "chuva": false
        }
        }
        
        ira validar os dados e inserir no banco, caso estejam corretos. 
        ira iniciar a irrigação se necessário.
        
        Quando o assunto for irrigacao, espera os campos:
        - no (identificador do nó)
        
        Exemplo de mensagem esperada:
        {
        "no": "3o8083c0-5f89-4a8f-b554-6af32a60cb3c",
        "assunto": "irrigacao",
        "dados": {
            "no_atuante": "3b8073c0-5f89-4a8f-b554-6af32a60cb2d",
            "status_irrigacao": "ativa",
            "hora_inicio": "adicionar dia e hora",
            "hora_fim": "adicionar dia e hora"
        }
        }
        """
        while True:
            msg = self._lora.read_message()
            if msg:
                try:
                    msg = msg.strip()
                    if not msg:
                        self._log.warn("Mensagem vazia recebida via LoRa")
                        continue

                    pacote = json.loads(msg)
                    assunto = pacote.get("assunto", "").strip()
                    identificador_no = pacote.get("no", "").strip()
                    dados = pacote.get("dados", {})
                    resultado = self._acoes_db.buscar_no_por_id(identificador_no, self._coletor_id)

                    if assunto == "coleta":
                        if not self._valida.valida_insert(dados):
                            self._log.info(f"Dados incompletos ou inválidos: {dados}")
                            self._lora.send_nok()
                            continue

                        if resultado:
                            no_id = resultado[0]
                            temp = dados.get("temperatura")
                            umi_solo = dados.get("umidade_solo")
                            umi_ar = dados.get("umidade_ar")
                            chuva = dados.get("chuva")

                            self._insere_dados(temp, umi_solo, umi_ar, chuva, no_id)

                        irriga = self._define_irrigacao.definir_irrigacao(umi_solo, chuva)
                        if irriga:
                            self._lora.send_turn_on_irrigation(no_id)

                    elif assunto == "irrigacao":
                        if resultado:
                            no_id = resultado[0]
                            no_atuante = dados.get("no_atuante")
                            hora_inicio = dados.get("hora_inicio")
                            hora_fim = dados.get("hora_fim")

                            if hora_fim is not None:
                                self._acoes_db.atualizar_fim_irrigacao(no_id, hora_fim)
                            else:
                                self._acoes_db.inserir_dados_irrigacao(
                                    no_id=no_id,
                                    no_atuante=no_atuante,
                                    inicio=hora_inicio,
                                    fim=None
                                )
                    else:
                        self._log.warn(f"Nó '{identificador_no}' não encontrado")

                except json.JSONDecodeError:
                    self._log.error(f"JSON inválido: {msg}")

                self._log.info(f"Recebido: {msg}")
            time.sleep(0.1)