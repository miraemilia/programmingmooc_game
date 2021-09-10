import pygame

def laske_korkeus(kuvan_nimi: str):
    return kuvan_nimi.get_height()

def laske_leveys(kuvan_nimi: str):
    return kuvan_nimi.get_width()

class Morko:
    def __init__(self, aloituspiste: list, lopetuspiste: list, nopeus: int):
        self.aloituspiste = aloituspiste
        self.lopetuspiste = lopetuspiste
        self.nopeus = nopeus

        self.paikka = []
        self.paikka.append(self.aloituspiste[0])
        self.paikka.append(self.aloituspiste[1])
    
        self.kuva = pygame.image.load("hirvio.png")
        self.leveys = laske_leveys(self.kuva)
        self.korkeus = laske_korkeus(self.kuva)
        
        self.tormayksia = 0

    def liikkuu(self):
        if self.paikka[0] == self.aloituspiste[0] or self.paikka[0] == self.lopetuspiste[0]:
            self.nopeus = -self.nopeus
        self.paikka[0] += self.nopeus*2
        if self.aloituspiste[1] != self.lopetuspiste[1]:
            self.paikka[1] -= self.nopeus

    def tormays(self, kuva_x:int, kuva_y: int, leveys: int, korkeus: int):
        if kuva_x + leveys/2 in range(self.paikka[0], self.paikka[0] + self.leveys):
            if kuva_y + korkeus/2 in range(self.paikka[1], self.paikka[1] + self.korkeus):
                self.tormayksia += 1

class Kolikko:
    def __init__(self, paikka: tuple):
        self.kuva = pygame.image.load("kolikko.png")
        self.leveys = laske_leveys(self.kuva)
        self.korkeus = laske_korkeus(self.kuva)
        self.keski = int(self.leveys/2)
        self.paikalla = True
        self.paikka = (paikka[0] - self.keski, paikka[1])
        self.poimittu = 0

    def poimi(self, kuva_x: int, kuva_y: int, leveys: int, korkeus: int):
        if kuva_x+leveys/2 in range(self.paikka[0], self.paikka[0] + self.leveys):
            if kuva_y+korkeus/2 in range(self.paikka[1], self.paikka[1] + self.korkeus):
                self.paikalla = False
                self.poimittu = 1

class Peli:
    def __init__(self):
        pygame.init()

        #näytön mitat
        self.leveys = 600
        self.korkeus = 700
        self.palkin_korkeus = 100
        self.aukko = 150

        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        pygame.display.set_caption("Mörkösokkelo")

        #fontit ja värit
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.fontti_pieni = pygame.font.SysFont("Arial", 16)
        self.taustavari = (0, 100, 200)
        self.kirjoitusvari = (0, 0, 255)

        self.kello = pygame.time.Clock()

        #robotin kuva ja mitat
        self.robo_kuva = pygame.image.load("robo.png")
        self.korkeus_robo = laske_korkeus(self.robo_kuva)
        self.leveys_robo = laske_leveys(self.robo_kuva)

        #oven kuva, mitat ja paikka
        self.ovi_kuva = pygame.image.load("ovi.png")
        self.korkeus_ovi = laske_korkeus(self.ovi_kuva)
        self.leveys_ovi = laske_leveys(self.ovi_kuva)
        self.x_ovi = self.osio(5) - self.leveys_ovi/2
        self.y_ovi = 0

        self.uusi_peli()

    def uusi_peli(self):
        
        self.vasemmalle = False
        self.oikealle = False
        self.ylos = False
        self.alas = False

        self.alkuasetukset()
        self.silmukka()
        self.lopeta()

    def osio(self, kuudenneksen_numero: int):
        return int((self.leveys/6)*kuudenneksen_numero)

    def alkuasetukset(self):

        # robotin alkukoordinaatit vasemmanpuolisen käytävän keskellä alareunassa
        self.robo = [self.osio(1)-self.leveys_robo/2, self.korkeus-self.palkin_korkeus-self.korkeus_robo]

        #mörköoliot
        morko1 = Morko((150, 330), (0, 330), 1)
        morko2 = Morko((350, 0), (200, 150), 1)
        morko3 = Morko((200, 350), (350, 350), -1)
        morko4 = Morko((380, 440), (550, 540), -1)
        morko5 = Morko((540, 100), (400, 100), 2)
        self.morot = [morko1, morko2, morko3, morko4, morko5]

        #kolikko-oliot
        kolikko0 = Kolikko((self.osio(1), 450))
        kolikko1 = Kolikko((self.osio(1), 200))
        kolikko2 = Kolikko((self.osio(3), 300))
        kolikko3 = Kolikko((self.osio(3), 500))
        kolikko4 = Kolikko((self.osio(5), 250))
        self.kolikot = [kolikko0, kolikko1, kolikko2, kolikko3, kolikko4]

        #pisteenlaskun alkutilanne
        self.kolikoita = 0
        self.tormayksia = 0
        self.aika = 0
        self.pisteet = 0

    def piirra_viiva(self, aloitus: tuple, lopetus: tuple):
        pygame.draw.line(self.naytto, self.kirjoitusvari, aloitus, lopetus, 4)

    def alapalkki(self):
        aloituskorkeus = self.korkeus - self.palkin_korkeus +15
        pygame.draw.rect(self.naytto, (0, 0, 0), (0, self.korkeus-self.palkin_korkeus, self.korkeus-self.palkin_korkeus, self.korkeus))

        #kolikot
        for i in range(self.kolikoita):
            self.naytto.blit(self.kolikot[0].kuva, (10 + i*15, aloituskorkeus - 10))
        
        #törmäykset
        pygame.draw.rect(self.naytto, (255, 0 , 0), (150, aloituskorkeus -5, 80, 35))
        self.naytto.blit(self.morot[0].kuva, (137, aloituskorkeus -5))
        tormaykset = self.fontti.render(f"-{self.tormayksia}", True, self.kirjoitusvari)
        self.naytto.blit(tormaykset, (185, aloituskorkeus))

        #ajastin
        minuutteja = self.aika // 3600
        sekunteja = (self.aika - minuutteja*3600) // 60
        ajastin = self.fontti.render(f"{minuutteja:02}:{sekunteja:02}", True, self.kirjoitusvari)
        self.naytto.blit(ajastin, (270, aloituskorkeus))
        
        #pistelaskuri
        pygame.draw.rect(self.naytto, (255, 255 , 255), (445, aloituskorkeus, 140, 27))
        pistelaskuri = self.fontti.render(f"Pisteet: {self.pisteet}", True, self.kirjoitusvari)
        self.naytto.blit(pistelaskuri, (450, aloituskorkeus))

        #ohje
        ohje = self.fontti_pieni.render("Kerää kolikot mahdollisimman nopeasti ja vältä törmäämästä mörköihin matkalla.", True, self.kirjoitusvari)
        ohje2 = self.fontti_pieni.render("Aloita uusi peli välilyönnillä.", True, self.kirjoitusvari)
        self.naytto.blit(ohje, (10, aloituskorkeus + 35))
        self.naytto.blit(ohje2, (10, aloituskorkeus + 55))

    def ovi(self):
        #palauttaa True, jos robotti on ovella
        if self.robo[1] in range(self.y_ovi, self.y_ovi + 20):
            if self.robo[0] >= self.x_ovi - 10 and self.robo[0] + self.leveys_robo <= self.x_ovi + self.leveys_ovi + 10:
                self.loppupisteet = self.pisteet
                return True
            else:
                return False
        else:
            return False

    def lopeta(self):
        #infolaatikko
        pygame.draw.rect(self.naytto, (255, 255, 255), (150, 200, 300, 200))
        
        if self.pisteet < 0:
            havioteksti = self.fontti.render(f"Böö! Hävisit!", True, self.kirjoitusvari)
            self.naytto.blit(havioteksti, (220, 280))
            self.naytto.blit(self.morot[0].kuva, (350, 280))

        else:
            voittoteksti = self.fontti.render(f"Sait {self.loppupisteet} pistettä!", True, self.kirjoitusvari)
            self.naytto.blit(voittoteksti, (220, 280))

        pygame.display.flip()

        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_SPACE:
                        self.uusi_peli()
        
    def silmukka(self):
        while not(self.pisteet < 0 or self.ovi() == True):

            self.tutki_tapahtumat()

            #tarkistaa kolikoiden tilan
            for kolikko in self.kolikot:
                if kolikko.paikalla:
                    kolikko.poimi(self.robo[0], self.robo[1], self.leveys_robo, self.korkeus_robo)
            self.kolikoita = len([kolikko for kolikko in self.kolikot if kolikko.paikalla == False])

            #tarkistaa ja laskee törmäykset
            for morko in self.morot:
                morko.liikkuu()
                morko.tormays(self.robo[0], self.robo[1], self.leveys_robo, self.korkeus_robo) 
            self.tormayksia = sum([morko.tormayksia for morko in self.morot])

            #pistetilanne
            self.pisteet = 25* self.kolikoita - (self.aika // 600) - self.tormayksia

            self.aika += 1

            self.paivita_naytto()

            self.kello.tick(60)


    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()
            if tapahtuma.type == pygame.KEYDOWN:
                #uusi peli
                if tapahtuma.key == pygame.K_SPACE:
                    self.alkuasetukset()
                #liikkuminen
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = True
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False

        if self.oikealle:
            # ensimmäinen väliseinä
            if self.robo[0] + self.leveys_robo in range(int(self.leveys/3), int(self.leveys/3)+4) and self.robo[1] > self.aukko - self.korkeus_robo:
                pass
            #toinen väliseinä
            elif self.robo[0] + self.leveys_robo in range(int(self.leveys/3*2), int(self.leveys/3*2)+4) and self.robo[1] < self.korkeus - self.palkin_korkeus - self.aukko:
                pass
            #oikea laita
            elif self.robo[0] + self.leveys_robo >= self.leveys:
                pass
            else:
                self.robo[0] +=2
        if self.vasemmalle:
            # ensimmäinen väliseinä
            if self.robo[0] in range(int(self.leveys/3), int(self.leveys/3)+4) and self.robo[1] > self.aukko - self.korkeus_robo:
                pass
            #toinen väliseinä
            elif self.robo[0] in range(int(self.leveys/3*2), int(self.leveys/3*2)+4) and self.robo[1] < self.korkeus - self.palkin_korkeus - self.aukko:
                pass
            # vasen laita
            elif self.robo[0] <= 0:
                pass
            else:
                self.robo[0] -=2
        if self.alas:
            #palkin päällä
            if self.robo[0] in range(int(self.leveys/3) - self.leveys_robo, int(self.leveys/3)+4) and self.robo[1] >= self.aukko - self.korkeus_robo:
                pass
            #pelialueen alareuna
            elif self.robo[1] + self.korkeus_robo <= self.korkeus - self.palkin_korkeus:   
                self.robo[1] += 2
        if self.ylos:
            # palkin alla
            if self.robo[0] in range(int(self.leveys/3*2) - self.leveys_robo, int(self.leveys/3*2)+4) and self.robo[1] < self.korkeus - self.palkin_korkeus - self.aukko:
                pass
            #pelialueen yläreuna
            elif self.robo[1] >= 2:
                self.robo[1] -= 2

    def paivita_naytto(self):
        self.naytto.fill(self.taustavari)
        self.piirra_viiva((self.leveys/3, self.aukko), (self.leveys/3, self.korkeus-self.palkin_korkeus))
        self.piirra_viiva(((self.leveys/3)*2, 0), ((self.leveys/3)*2, self.korkeus-self.palkin_korkeus-self.aukko))
        self.naytto.blit(self.ovi_kuva, (self.x_ovi, self.y_ovi))
        self.naytto.blit(self.robo_kuva, (self.robo[0], self.robo[1]))
        for morko in self.morot:
            self.naytto.blit(morko.kuva, (morko.paikka[0], morko.paikka[1]))
        for kolikko in self.kolikot:
            if kolikko.paikalla:
                self.naytto.blit(kolikko.kuva, kolikko.paikka)
        self.alapalkki()
        pygame.display.flip()

Peli()