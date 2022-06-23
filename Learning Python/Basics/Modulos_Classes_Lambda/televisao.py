class Televisao:
    def __init__(self):
        self.ligada = False
        self.canal = 5
    def power(self):
        self.ligada = not self.ligada
    def aumenta_canal(self):
        if self.ligada:
            self.canal += 1
    def diminui_canal(self):
        if self.ligada:
            self.canal -= 1


if __name__ == '__main__':
    televisao = Televisao() #instanciada false - desligada
    # toggle on off
    print("tv ligada", televisao.ligada)
    televisao.power() # liguei
    print("tv ligada: {}".format(televisao.ligada))
    # troca de canais
    print("canal: {}".format(televisao.canal))
    televisao.aumenta_canal()
    televisao.aumenta_canal()
    print("canal: {}".format(televisao.canal))
    televisao.diminui_canal()
    print("canal: {}".format(televisao.canal))