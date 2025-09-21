class DefineIrrigacao:
    def __init__(self):
        pass

    def definir_irrigacao(self, umidade_solo, chuva):
        # Lógica para definir a irrigação com base nos dados do solo e clima
        if chuva is True:
            return False  # Não iniciar irrigação se estiver chovendo
        else:
            if umidade_solo < 60:
                return True  # Iniciar irrigação
            if umidade_solo >= 80:
                return False  # Não iniciar irrigação