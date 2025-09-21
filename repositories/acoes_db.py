from infra.db import Database

class AcoesDB:
    def __init__(self):
        self._db = Database()
    
    def inserir_dados_coletados(self, coletor_id, no_id, temperatura, umidade_solo, umidade_ar, chuva):
        self._db.execute_ddl_false("""
            INSERT INTO dados_coletados (
                coletor_id, no_id, temperatura, umidade_solo, umidade_ar, chuva
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (coletor_id, no_id, temperatura, umidade_solo, umidade_ar, chuva))
    
    def buscar_no_por_id(self, no_id, coletor_id):
        resultado = self._db.execute_ddl_true("""
            SELECT id FROM nos
            WHERE id = %s AND coletor_id = %s
        """, (no_id, coletor_id))
        return resultado[0] if resultado else None
    
    def inserir_dados_irrigacao(self, no_id, no_atuante, inicio, fim):
        """insere um novo registro de irrigação
        no_id: id do nó que gerencia a ação da irrigação(que liga a bomba)
        no_atuante: id do nó atuante (setor que esta sendo irrigado)
        inicio: timestamp do início da irrigação
        fim: timestamp do fim da irrigação (pode ser None se estiver em andamento)
        """
        self._db.execute_ddl_false("""
            INSERT INTO dados_irrigacao (
                no_id, no_atuante, inicio, fim
            ) VALUES (%s, %s, %s, %s)
        """, (no_id, no_atuante, inicio, fim))
        
    def atualizar_fim_irrigacao(self, no_id, no_atuante, fim):
        """atualiza o campo fim de uma irrigação"""
        self._db.execute_ddl_false("""
            UPDATE dados_irrigacao
            SET fim = %s
            WHERE no_id = %s and no_atuante = %s AND fim IS NULL
        """, (fim, no_id, no_atuante))
    
    def buscar_irrigacao_ativa(self, no_id):
        """busca se há uma irrigação ativa (sem fim) para o nó que gerencia a acao da irrigacao"""
        resultado = self._db.execute_ddl_true("""
            SELECT id, inicio FROM dados_irrigacao
            WHERE no_id = %s AND fim IS NULL
        """, (no_id,))
        return resultado[0] if resultado else None
    
    
    # TODO: criar tabela que relacione no gestor de irrigação com os nós atuantes