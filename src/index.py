from varasto import Varasto

def aloitus_varasto(mehua, olutta):
 print("Luonnin jälkeen:")
 print(f"Mehuvarasto: {mehua}")
 print(f"Olutvarasto: {olutta}")

def olut_getterit(olutta):
 print("Olut getterit:")
 print(f"saldo = {olutta.saldo}")
 print(f"tilavuus = {olutta.tilavuus}")
 print(f"paljonko_mahtuu = {olutta.paljonko_mahtuu()}")

def mehu_setter(mehua):
 print("Mehu setterit:")
 print("Lisätään 50.7")
 mehua.lisaa_varastoon(50.7)
 print(f"Mehuvarasto: {mehua}")
 print("Otetaan 3.14")
 mehua.ota_varastosta(3.14)
 print(f"Mehuvarasto: {mehua}")

def virhetilanteet():
 print("Virhetilanteita:")
 print("Varasto(-100.0);")
 huono = Varasto(-100.0)
 print(huono)

 print("Varasto(100.0, -50.7)")
 huono = Varasto(100.0, -50.7)
 print(huono)

def taysi_varasto(olutta):
 print(f"Olutvarasto: {olutta}")
 print("olutta.lisaa_varastoon(1000.0)")
 olutta.lisaa_varastoon(1000.0)
 print(f"Olutvarasto: {olutta}")

 print(f"Olutvarasto: {olutta}")
 print("olutta.ota_varastosta(1000.0)")
 saatiin = olutta.ota_varastosta(1000.0)
 print(f"saatiin {saatiin}")
 print(f"Olutvarasto: {olutta}")

def negatiivinen_varasto(mehua):
 print(f"Mehuvarasto: {mehua}")
 print("mehua.lisaa_varastoon(-666.0)")
 mehua.lisaa_varastoon(-666.0)
 print(f"Mehuvarasto: {mehua}")

 print(f"Mehuvarasto: {mehua}")
 print("mehua.otaVarastosta(-32.9)")
 saatiin = mehua.ota_varastosta(-32.9)
 print(f"saatiin {saatiin}")
 print(f"Mehuvarasto: {mehua}")

def main():
 mehua = Varasto(100.0)
 olutta = Varasto(100.0, 20.2)

 aloitus_varasto(mehua, olutta)
 olut_getterit(olutta)
 mehu_setter(mehua)
 virhetilanteet()
 taysi_varasto(olutta)
 negatiivinen_varasto(mehua)

if __name__ == "__main__":
 main()
