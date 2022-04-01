import pygame, sys, random
from pygame import mixer, Rect

#-----------------Setup do jogo-----------------------------
pygame.init() #Inicializa pygame
clock = pygame.time.Clock() #define a velocidade dos frames
cont_jogador = 0
cont_oponente = 0

#-----------------Setup da janela----------------------------
largura_tela = 1280
altura_tela = 960
tela = pygame.display.set_mode((largura_tela,altura_tela))
pygame.display.set_caption('Pongue')
bg_cor = pygame.Color('grey12') #fundo da tela
cinza_claro = (200,200,200)     #cor dos componentes
fonte = pygame.font.Font('Kemco Pixel Bold.ttf', 144) # Scores

# ---------Configuração da bola e dos jogadores----------------
bola: Rect = pygame.Rect(largura_tela/2 - 15,10,30,30)
jogador = pygame.Rect(largura_tela - 20,altura_tela/2-70,10,140)
oponente = pygame.Rect(10,altura_tela/2-70,10,140)

bola_vel_x = 10 * random.choice((1,-1))  #Velocidade da bola no eixo x e y
bola_vel_y = 10 * random.choice((1,-1))
jogador_vel = 0
oponente_vel = 50

bola_som = mixer.Sound('sfx_movement_ladder1b.wav')
som_derrota = mixer.Sound('sfx_sound_shutdown1.wav')

delay = None
#-----------------Funções-----------------------------------

def bola_movimentos(): # Define a direção da bola no jogo
    global bola_vel_x,bola_vel_y,cont_jogador,cont_oponente, delay
    bola.x += bola_vel_x
    bola.y += bola_vel_y

    if bola.top <= 0 or bola.bottom >= altura_tela:  # eixo vertical
        bola_vel_y *= -1
        bola_som.play()

    if bola.left <= 0:  # eixo horizontal
        bola_vel_x *= -1
        som_derrota.play()
        cont_jogador += 1
        delay = pygame.time.get_ticks()

    if bola.right >= largura_tela:
        bola_vel_x *= -1
        cont_oponente += 1
        som_derrota.play()
        delay = pygame.time.get_ticks()

    if bola.colliderect((jogador)) and bola_vel_x > 0:
        bola_som.play()
        if abs(bola.right - jogador.left) < 10:
            bola_vel_x *= -1
        elif abs(bola.bottom - jogador.top) < 10 and bola_vel_y > 0:
            bola_vel_y *= -1
        elif abs(bola.top - jogador.bottom) < 10 and bola_vel_y < 0:
            bola_vel_y *= -1

    if bola.colliderect((oponente)) and bola_vel_x < 0:
        bola_som.play()
        if abs(bola.left - oponente.right) < 10:
            bola_vel_x *= -1
        elif abs(bola.bottom - oponente.top) < 10 and bola_vel_y > 0:
            bola_vel_y *= -1
        elif abs(bola.top - oponente.bottom) < 10 and bola_vel_y < 0:
            bola_vel_y *= -1

def contador():
    pont_jogador = fonte.render(str(cont_jogador), True, (200, 200, 200))
    tela.blit(pont_jogador, (690, 50))
    pont_oponente = fonte.render(str(cont_oponente), True, (200, 200, 200))
    tela.blit(pont_oponente, (500, 50))

def jogador_movimentos(): #Define os movimentos do jogador
    jogador.y += jogador_vel
    if jogador.top <= 0:
        jogador.top = 0
    if jogador.bottom >= altura_tela:
        jogador.bottom = altura_tela

def oponente_AI(): #Define os movimentos do oponente
    if oponente.top < bola.y:
        oponente.top += oponente_vel
    if oponente.bottom > bola.y:
        oponente.bottom -= oponente_vel
    if oponente.top <= 0:
        oponente.top = 0
    if oponente.bottom >= altura_tela:
        oponente.bottom = altura_tela

def restart_bola(): #Reinicia o jogo quando um perde a bola
    global bola_vel_x,bola_vel_y,delay

    tempo_atual = pygame.time.get_ticks()
    bola.center = (largura_tela / 2, altura_tela/2)
    if  tempo_atual - delay < 1500:
        bola_vel_x,bola_vel_y = 0,0
    else:
        bola_vel_y = 10 * random.choice((1,-1))
        bola_vel_x = 10 * random.choice((1, -1))
        delay =None

def jogo_config():
    pygame.draw.rect(tela, cinza_claro, jogador)
    pygame.draw.rect(tela, cinza_claro, oponente)
    pygame.draw.ellipse(tela, cinza_claro, bola)
    pygame.draw.aaline(tela, cinza_claro, (largura_tela / 2, 0), (largura_tela / 2, altura_tela))

#----------------Fim configuração----------------------

while True:

    #Valores de entrada
    for evento in pygame.event.get():          #Quando uma tecla é pressionada
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:   #Teclas pressionadas
            if evento.key == pygame.K_DOWN:
                jogador_vel +=20
            if evento.key == pygame.K_UP:
                jogador_vel -=20
        if evento.type == pygame.KEYUP:         #Quando uma tecla é solta
           if evento.key == pygame.K_DOWN:
                jogador_vel -=20
           if evento.key == pygame.K_UP:
             jogador_vel +=20

    jogador_movimentos()
    oponente_AI()
    bola_movimentos()
    #Visual - imprime na tela os componentos do jogo e as caracteristicas dos mesmo(Cor, tamanho)
    tela.fill(bg_cor)
    contador()
    jogo_config()
    if delay:
        restart_bola()
    # Atualização da tela
    pygame.display.flip()
    clock.tick(60)
