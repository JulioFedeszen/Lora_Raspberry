class ValidaDados:
    def valida_insert(self, dados):
        campos = ["temperatura", "umidade_solo", "umidade_ar", "chuva"]
        for campo in campos:
            if campo not in dados or dados[campo] in [None, ""]:
                return False
        return True