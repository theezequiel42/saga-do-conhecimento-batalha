import os
import pygame
import random
import asyncio
from questions import perguntas_por_nivel_e_disciplina

# Inicialização da Pygame
pygame.init()
pygame.mixer.init()

# Configurações da tela
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Saga do Conhecimento - Batalha")

# Cores
COLORS = {
    "BRANCO": (255, 255, 255),
    "PRETO": (0, 0, 0),
    "VERDE": (0, 255, 0),
    "VERMELHO": (255, 0, 0),
    "AZUL": (0, 0, 255),
    "CINZA": (169, 169, 169),
    "CINZA_CLARO": (211, 211, 211),
    "AMARELO": (255, 255, 0)
}

# Músicas
MUSICAS = {
    "menu": "musica_menu.mp3",
    "batalha": "musica_batalha.mp3",
    "vitoria": "som_vitoria.mp3",
    "derrota": "som_derrota.mp3",
    "historia": "musica_historia.mp3"
}

# Fonte
font = pygame.font.Font(None, 36)

# Carregar e redimensionar imagens
def carregar_imagem(caminho, largura, altura):
    try:
        imagem = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(imagem, (largura, altura))
    except pygame.error as e:
        print(f"Erro ao carregar imagem: {caminho}\n{e}")
        return pygame.Surface((largura, altura))  # Retorna uma superfície vazia como fallback

background_batalha_img = carregar_imagem("background_batalha.png", WIDTH, HEIGHT)
background_menu_img = carregar_imagem("background_menu.png", WIDTH, HEIGHT)
background_historia_img = carregar_imagem("background_historia.png", WIDTH, HEIGHT)

# Funções de utilidade
def tocar_musica(musica):
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play(-1)  # Loop infinito

def parar_musica():
    pygame.mixer.music.stop()

def tocar_som(som):
    efeito = pygame.mixer.Sound(som)
    efeito.play()

def desenhar_texto(texto, fonte, cor, superficie, x, y):
    objeto_texto = fonte.render(texto, True, cor)
    retangulo_texto = objeto_texto.get_rect(topleft=(x, y))
    superficie.blit(objeto_texto, retangulo_texto)
    return retangulo_texto  # Retornar o retângulo para detecção de clique

def desenhar_hud(screen, estado):
    # Barra de saúde do jogador
    pygame.draw.rect(screen, COLORS["VERMELHO"], (20, 600, 200, 20))
    pygame.draw.rect(screen, COLORS["VERDE"], (20, 600, 2 * estado.saude_jogador, 20))
    desenhar_texto(f"Jogador: {estado.saude_jogador}/100", font, COLORS["BRANCO"], screen, 20, 570)

    # Barra de saúde do inimigo
    pygame.draw.rect(screen, COLORS["VERMELHO"], (1060, 600, 200, 20))
    pygame.draw.rect(screen, COLORS["VERDE"], (1060, 600, 2 * estado.saude_inimigo, 20))
    desenhar_texto(f"Inimigo: {estado.saude_inimigo}/100", font, COLORS["BRANCO"], screen, 1060, 570)

    # Barra de mana do jogador
    pygame.draw.rect(screen, COLORS["CINZA"], (20, 660, 200, 20))
    pygame.draw.rect(screen, COLORS["AZUL"], (20, 660, 2 * estado.mana_jogador, 20))
    desenhar_texto(f"Mana: {estado.mana_jogador}/100", font, COLORS["BRANCO"], screen, 20, 630)

    # Barra de mana do inimigo
    pygame.draw.rect(screen, COLORS["CINZA"], (1060, 660, 200, 20))
    pygame.draw.rect(screen, COLORS["AZUL"], (1060, 660, 2 * estado.mana_inimigo, 20))
    desenhar_texto(f"Mana: {estado.mana_inimigo}/100", font, COLORS["BRANCO"], screen, 1060, 630)

    # Pontos de sabedoria
    desenhar_texto(f"Pontos de Sabedoria: {estado.pontos_sabedoria}", font, COLORS["BRANCO"], screen, WIDTH - 320, 20)

def desenhar_personagens(screen, jogador_animacoes, inimigo_animacoes, estado):
    jogador_pos = (100, 300)  # Ajustar posição do jogador mais para baixo
    inimigo_pos = (980, 300)  # Ajustar posição do inimigo mais para baixo

    # Animação do jogador
    frames = jogador_animacoes[estado.jogador_acao]
    frame_delay = 100  # Ajuste a velocidade da animação (menor valor para mais rápido)

    screen.blit(frames[estado.jogador_frame_atual], jogador_pos)
    estado.jogador_frame_tempo += 1
    if estado.jogador_frame_tempo >= frame_delay:
        estado.jogador_frame_tempo = 0
        estado.jogador_frame_atual = (estado.jogador_frame_atual + 1) % len(frames)
        if estado.jogador_acao == "attack" and estado.jogador_frame_atual == 0:
            estado.jogador_acao = "idle"  # Voltar para o estado idle após o ataque

    # Animação do inimigo
    frames = inimigo_animacoes[estado.inimigo_acao]
    frame_delay = 100

    screen.blit(frames[estado.inimigo_frame_atual], inimigo_pos)
    estado.inimigo_frame_tempo += 1
    if estado.inimigo_frame_tempo >= frame_delay:  # Ajuste a velocidade da animação (maior valor para mais devagar)
        estado.inimigo_frame_tempo = 0
        estado.inimigo_frame_atual = (estado.inimigo_frame_atual + 1) % len(frames)

def desenhar_barra_tempo(screen, tempo_restante, tempo_total):
    largura_barra = int((tempo_restante / tempo_total) * 400)
    pygame.draw.rect(screen, COLORS["AZUL"], (440, 80, largura_barra, 20))

def carregar_animacao(caminho, largura_frame, altura_frame, num_frames):
    try:
        sprite_sheet = pygame.image.load(caminho).convert_alpha()
    except pygame.error as e:
        print(f"Erro ao carregar animação: {caminho}\n{e}")
        return [pygame.Surface((largura_frame, altura_frame)) for _ in range(num_frames)]
    
    largura_sheet, altura_sheet = sprite_sheet.get_size()
    largura_frame = largura_sheet // num_frames  # Atualiza a largura do frame de acordo com o número de quadros
    
    frames = []
    for i in range(num_frames):
        frame = sprite_sheet.subsurface((i * largura_frame, 0, largura_frame, altura_frame))
        frames.append(pygame.transform.scale(frame, (200, 200)))
    return frames

class EstadoJogo:
    def __init__(self):
        self.saude_jogador = 100
        self.saude_inimigo = 100
        self.mana_jogador = 100
        self.mana_inimigo = 100
        self.pontos_sabedoria = 0
        self.defendendo = False
        self.nivel_selecionado = "1° Ano"
        self.disciplinas_selecionadas = ["Matemática", "Língua Portuguesa"]
        self.batalha_ativa = True
        self.jogador_acao = "idle"
        self.jogador_frame_atual = 0
        self.jogador_frame_tempo = 0
        self.inimigo_frame_atual = 0
        self.inimigo_frame_tempo = 0
        self.inimigo_acao = "Deceased_idle"

estado = EstadoJogo()

# Carregar animação do jogador e do inimigo
jogador_animacoes = {
    "idle": carregar_animacao("idle-Sheet.png", 64, 64, 4),
    "run": carregar_animacao("Run-Sheet.png", 64, 64, 6),
    "attack": carregar_animacao("Attack-01-Sheet.png", 64, 64, 8),
    "derrota": carregar_animacao("derrota_jogador-Sheet.png", 64, 64, 8)
}

inimigo_animacoes = {
    "idle": carregar_animacao("Idle-Sheet-inimigo.png", 64, 64, 4),
    "Deceased_idle": carregar_animacao("Deceased_idle-Sheet.png", 48, 48, 4),
    "Deceased_walk": carregar_animacao("Deceased_walk-Sheet.png", 48, 48, 4),
    "Deceased_hurt": carregar_animacao("Deceased_hurt-Sheet.png", 48, 48, 4),
    "Deceased_death": carregar_animacao("Deceased_death-Sheet.png", 48, 48, 4),
    "Deceased_attack": carregar_animacao("Deceased_attack-Sheet.png", 48, 48, 4)
}

# Função para selecionar nível e disciplina
def selecionar_nivel_e_disciplina():
    global estado
    screen.blit(background_menu_img, (0, 0))
    desenhar_texto("Selecione o Nível:", font, COLORS["BRANCO"], screen, 20, 20)
    niveis = list(perguntas_por_nivel_e_disciplina.keys())
    retangulos_niveis = []
    for i, nivel in enumerate(niveis):
        retangulo = desenhar_texto(f"{i+1}. {nivel}", font, COLORS["BRANCO"], screen, 20, 60 + i * 40)
        retangulos_niveis.append(retangulo)
    ret_voltar_nivel = desenhar_texto("Voltar ao Menu", font, COLORS["BRANCO"], screen, WIDTH - 200, HEIGHT - 50)
    pygame.display.flip()

    opcao_selecionada = 0
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % (len(retangulos_niveis) + 1)
                elif evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % (len(retangulos_niveis) + 1)
                elif evento.key == pygame.K_RETURN:
                    if opcao_selecionada < len(niveis):
                        estado.nivel_selecionado = niveis[opcao_selecionada]
                        selecionar_disciplina()
                        return
                    else:
                        tela_inicial()
                        return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ret_voltar_nivel.collidepoint(evento.pos):
                    tela_inicial()
                    return
                for i, ret in enumerate(retangulos_niveis):
                    if ret.collidepoint(evento.pos):
                        estado.nivel_selecionado = niveis[i]
                        selecionar_disciplina()
                        return
        for i, ret in enumerate(retangulos_niveis):
            if ret.collidepoint(mouse_pos):
                opcao_selecionada = i
        if ret_voltar_nivel.collidepoint(mouse_pos):
            opcao_selecionada = len(niveis)
        screen.blit(background_menu_img, (0, 0))
        desenhar_texto("Selecione o Nível:", font, COLORS["BRANCO"], screen, 20, 20)
        for i, nivel in enumerate(niveis):
            cor = COLORS["PRETO"] if i == opcao_selecionada else COLORS["BRANCO"]
            if i == opcao_selecionada:
                pygame.draw.rect(screen, COLORS["AMARELO"], retangulos_niveis[i])
            desenhar_texto(f"{i+1}. {nivel}", font, cor, screen, 20, 60 + i * 40)
        cor = COLORS["PRETO"] if opcao_selecionada == len(niveis) else COLORS["BRANCO"]
        if opcao_selecionada == len(niveis):
            pygame.draw.rect(screen, COLORS["AMARELO"], ret_voltar_nivel)
        desenhar_texto("Voltar ao Menu", font, cor, screen, WIDTH - 200, HEIGHT - 50)
        pygame.display.flip()

# Função para selecionar disciplina
def selecionar_disciplina():
    global estado
    screen.blit(background_menu_img, (0, 0))
    desenhar_texto("Selecione a Disciplina:", font, COLORS["BRANCO"], screen, 20, 20)
    disciplinas = ["Todas as Disciplinas"] + list(perguntas_por_nivel_e_disciplina[estado.nivel_selecionado].keys())
    retangulos_disciplinas = []
    for i, disciplina in enumerate(disciplinas):
        retangulo = desenhar_texto(f"{i+1}. {disciplina}", font, COLORS["BRANCO"], screen, 20, 60 + i * 40)
        retangulos_disciplinas.append(retangulo)
    ret_voltar_disciplina = desenhar_texto("Voltar ao Nível", font, COLORS["BRANCO"], screen, WIDTH - 200, HEIGHT - 50)
    pygame.display.flip()

    opcao_selecionada = 0
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % (len(retangulos_disciplinas) + 1)
                elif evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % (len(retangulos_disciplinas) + 1)
                elif evento.key == pygame.K_RETURN:
                    if opcao_selecionada < len(disciplinas) - 1:
                        estado.disciplinas_selecionadas = [disciplinas[opcao_selecionada]]
                    elif opcao_selecionada == 0:
                        estado.disciplinas_selecionadas = list(perguntas_por_nivel_e_disciplina[estado.nivel_selecionado].keys())
                    else:
                        selecionar_nivel_e_disciplina()
                        return
                    return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ret_voltar_disciplina.collidepoint(evento.pos):
                    selecionar_nivel_e_disciplina()
                    return
                for i, ret in enumerate(retangulos_disciplinas):
                    if ret.collidepoint(evento.pos):
                        if i == 0:
                            estado.disciplinas_selecionadas = list(perguntas_por_nivel_e_disciplina[estado.nivel_selecionado].keys())
                        else:
                            estado.disciplinas_selecionadas = [disciplinas[i]]
                        return
        for i, ret in enumerate(retangulos_disciplinas):
            if ret.collidepoint(mouse_pos):
                opcao_selecionada = i
        if ret_voltar_disciplina.collidepoint(mouse_pos):
            opcao_selecionada = len(disciplinas)
        screen.blit(background_menu_img, (0, 0))
        desenhar_texto("Selecione a Disciplina:", font, COLORS["BRANCO"], screen, 20, 20)
        for i, disciplina in enumerate(disciplinas):
            cor = COLORS["PRETO"] if i == opcao_selecionada else COLORS["BRANCO"]
            if i == opcao_selecionada:
                pygame.draw.rect(screen, COLORS["AMARELO"], retangulos_disciplinas[i])
            desenhar_texto(f"{i+1}. {disciplina}", font, cor, screen, 20, 60 + i * 40)
        cor = COLORS["PRETO"] if opcao_selecionada == len(disciplinas) else COLORS["BRANCO"]
        if opcao_selecionada == len(disciplinas):
            pygame.draw.rect(screen, COLORS["AMARELO"], ret_voltar_disciplina)
        desenhar_texto("Voltar ao Nível", font, cor, screen, WIDTH - 200, HEIGHT - 50)
        pygame.display.flip()

# Função principal da batalha
async def batalha():
    global estado
    # Reiniciar variáveis de estado
    estado.saude_jogador = 100
    estado.saude_inimigo = 100
    estado.mana_jogador = 100
    estado.mana_inimigo = 100
    estado.pontos_sabedoria = 0
    estado.defendendo = False
    estado.batalha_ativa = True
    estado.inimigo_acao = "Deceased_idle"

    tocar_musica(MUSICAS["batalha"])

    perguntas = []
    for disciplina in estado.disciplinas_selecionadas:
        perguntas.extend(perguntas_por_nivel_e_disciplina[estado.nivel_selecionado][disciplina])

    screen.blit(background_batalha_img, (0, 0))
    desenhar_texto(f"Nível: {estado.nivel_selecionado}", font, COLORS["BRANCO"], screen, 20, 20)
    desenhar_texto(f"Disciplinas: {', '.join(estado.disciplinas_selecionadas)}", font, COLORS["BRANCO"], screen, 20, 60)
    pygame.display.flip()
    await asyncio.sleep(2)

    while estado.batalha_ativa:
        acao = await selecionar_acao()
        if acao == "Fugir":
            executar_acao(acao, False, 0)
            await tela_inicial()
            break
        pergunta, opcoes_rects = await apresentar_pergunta(perguntas, 10)
        resposta_correta, tempo_resposta = await avaliar_resposta(pergunta, opcoes_rects, 10)
        executar_acao(acao, resposta_correta, tempo_resposta)
        resultado = checar_fim_batalha()
        if resultado:
            estado.batalha_ativa = False
            parar_musica()
            tocar_som(MUSICAS["vitoria"] if resultado == "Vitória" else MUSICAS["derrota"])
            screen.blit(background_batalha_img, (0, 0))
            desenhar_hud(screen, estado)
            desenhar_personagens(screen, jogador_animacoes, inimigo_animacoes, estado)
            desenhar_texto(resultado, font, COLORS["BRANCO"], screen, WIDTH // 2 - 50, HEIGHT // 2)
            pygame.display.flip()
            await asyncio.sleep(3)
            await tela_inicial()
        else:
            turno_inimigo()
            resultado = checar_fim_batalha()
            if resultado:
                estado.batalha_ativa = False
                parar_musica()
                tocar_som(MUSICAS["vitoria"] if resultado == "Vitória" else MUSICAS["derrota"])
                screen.blit(background_batalha_img, (0, 0))
                desenhar_hud(screen, estado)
                desenhar_personagens(screen, jogador_animacoes, inimigo_animacoes, estado)
                desenhar_texto(resultado, font, COLORS["BRANCO"], screen, WIDTH // 2 - 50, HEIGHT // 2)
                pygame.display.flip()
                await asyncio.sleep(3)
                await tela_inicial()

# Função para selecionar ação
async def selecionar_acao():
    screen.blit(background_batalha_img, (0, 0))
    desenhar_hud(screen, estado)
    desenhar_personagens(screen, jogador_animacoes, inimigo_animacoes, estado)
    desenhar_texto("Escolha sua ação:", font, COLORS["BRANCO"], screen, 20, 20)
    ret_ataque = desenhar_texto("Ataque", font, COLORS["BRANCO"], screen, 20, 60)
    ret_magia = desenhar_texto("Magia", font, COLORS["BRANCO"], screen, 20, 100)
    ret_defesa = desenhar_texto("Defesa", font, COLORS["BRANCO"], screen, 20, 140)
    ret_curar = desenhar_texto("Curar", font, COLORS["BRANCO"], screen, 20, 180)
    ret_fugir = desenhar_texto("Fugir", font, COLORS["BRANCO"], screen, 20, 220)
    pygame.display.flip()

    acao_selecionada = None
    opcao_selecionada = 0
    retangulos_acoes = [ret_ataque, ret_magia, ret_defesa, ret_curar, ret_fugir]

    while acao_selecionada is None:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(retangulos_acoes)
                elif evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(retangulos_acoes)
                elif evento.key == pygame.K_RETURN:
                    acao_selecionada = ["Ataque", "Magia", "Defesa", "Curar", "Fugir"][opcao_selecionada]
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, ret in enumerate(retangulos_acoes):
                    if ret.collidepoint(evento.pos):
                        acao_selecionada = ["Ataque", "Magia", "Defesa", "Curar", "Fugir"][i]
            for i, ret in enumerate(retangulos_acoes):
                if ret.collidepoint(mouse_pos):
                    opcao_selecionada = i

        screen.blit(background_batalha_img, (0, 0))
        desenhar_hud(screen, estado)
        desenhar_personagens(screen, jogador_animacoes, inimigo_animacoes, estado)
        desenhar_texto("Escolha sua ação:", font, COLORS["BRANCO"], screen, 20, 20)
        for i, (texto, ret) in enumerate(zip(["Ataque", "Magia", "Defesa", "Curar", "Fugir"], retangulos_acoes)):
            cor = COLORS["PRETO"] if i == opcao_selecionada else COLORS["BRANCO"]
            if i == opcao_selecionada:
                pygame.draw.rect(screen, COLORS["AMARELO"], ret)
            desenhar_texto(texto, font, cor, screen, 20, 60 + i * 40)
        pygame.display.flip()
        await asyncio.sleep(0)

    return acao_selecionada

# Função para apresentar pergunta
async def apresentar_pergunta(perguntas, tempo_total):
    pergunta = random.choice(perguntas)
    screen.blit(background_batalha_img, (0, 0))
    desenhar_hud(screen, estado)
    desenhar_personagens(screen, jogador_animacoes, inimigo_animacoes, estado)
    desenhar_texto(pergunta["pergunta"], font, COLORS["BRANCO"], screen, 20, 20)
    desenhar_barra_tempo(screen, tempo_total, tempo_total)

    opcoes_rects = []
    for i, opcao in enumerate(pergunta["opcoes"]):
        ret_opcao = desenhar_texto(opcao, font, COLORS["BRANCO"], screen, 20, 120 + i * 30)
        opcoes_rects.append(pygame.Rect(20, 120 + i * 30, WIDTH - 40, 30))  # Área clicável
    pygame.display.flip()
    return pergunta, opcoes_rects

# Função para avaliar resposta
async def avaliar_resposta(pergunta, opcoes_rects, tempo_total):
    tempo_inicio = pygame.time.get_ticks()
    opcao_selecionada = None
    indice_opcao_selecionada = 0

    while opcao_selecionada is None:
        tempo_atual = pygame.time.get_ticks()
        tempo_passado = (tempo_atual - tempo_inicio) / 1000
        tempo_restante = tempo_total - tempo_passado

        if tempo_restante <= 0:
            break

        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    indice_opcao_selecionada = (indice_opcao_selecionada + 1) % len(opcoes_rects)
                elif evento.key == pygame.K_UP:
                    indice_opcao_selecionada = (indice_opcao_selecionada - 1) % len(opcoes_rects)
                elif evento.key == pygame.K_RETURN:
                    opcao_selecionada = indice_opcao_selecionada
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(opcoes_rects):
                    if rect.collidepoint(evento.pos):
                        opcao_selecionada = i
            for i, rect in enumerate(opcoes_rects):
                if rect.collidepoint(mouse_pos):
                    indice_opcao_selecionada = i

        # Atualizar cronômetro na tela
        screen.blit(background_batalha_img, (0, 0))
        desenhar_hud(screen, estado)
        desenhar_personagens(screen, jogador_animacoes, inimigo_animacoes, estado)
        desenhar_texto(pergunta["pergunta"], font, COLORS["BRANCO"], screen, 20, 20)
        for i, opcao in enumerate(pergunta["opcoes"]):
            cor = COLORS["PRETO"] if i == indice_opcao_selecionada else COLORS["BRANCO"]
            if i == indice_opcao_selecionada:
                pygame.draw.rect(screen, COLORS["CINZA_CLARO"], opcoes_rects[i])
            desenhar_texto(opcao, font, cor, screen, 20, 120 + i * 30)
        desenhar_barra_tempo(screen, tempo_restante, tempo_total)
        pygame.display.flip()
        await asyncio.sleep(0)

    tempo_total_resposta = (pygame.time.get_ticks() - tempo_inicio) / 1000

    if opcao_selecionada == pergunta["resposta"]:
        resposta_correta = True
    else:
        resposta_correta = False

    return resposta_correta, tempo_total_resposta

# Função para executar ação
def executar_acao(acao, resposta_correta, tempo_resposta):
    global estado
    dano = 0
    mensagem = ""
    dano_inimigo = False
    cura = 0

    if acao == "Fugir":
        estado.batalha_ativa = False
        mensagem = "Você fugiu da batalha!"
    else:
        if resposta_correta:
            if acao == "Ataque":
                if tempo_resposta <= 5:
                    dano = 20
                else:
                    dano = 10
                estado.jogador_acao = "attack"
                flash_effect(screen, COLORS["VERMELHO"], 100)
            elif acao == "Magia":
                if estado.mana_jogador >= 10:
                    estado.mana_jogador -= 10
                    if tempo_resposta <= 5:
                        dano = 25
                    else:
                        dano = 15
                    flash_effect(screen, COLORS["AZUL"], 100)
                else:
                    mensagem = "Mana insuficiente!"
            elif acao == "Defesa":
                estado.defendendo = True
                mensagem = "Você se preparou para a defesa!"
            elif acao == "Curar":
                if estado.mana_jogador >= 15:
                    estado.mana_jogador -= 15
                    if tempo_resposta <= 5:
                        cura = 20
                    else:
                        cura = 10
                    estado.saude_jogador = min(estado.saude_jogador + cura, 100)
                    mensagem = f"Você se curou em {cura} pontos!"
                else:
                    mensagem = "Mana insuficiente!"
            estado.pontos_sabedoria += 10
        else:
            if acao == "Defesa":
                estado.defendendo = False
                mensagem = "A defesa falhou!"
            else:
                mensagem = "Resposta errada! Nenhum dano causado!"

        screen.blit(background_batalha_img, (0, 0))
        desenhar_hud(screen, estado)
        desenhar_personagens(screen, jogador_animacoes, inimigo_animacoes, estado)
        pygame.display.flip()
        pygame.time.delay(500)
        
        if acao == "Ataque":
            for frame in jogador_animacoes["attack"]:
                screen.blit(background_batalha_img, (0, 0))
                desenhar_hud(screen, estado)
                screen.blit(frame, (100, 300))
                pygame.display.flip()
                pygame.time.delay(150)
            estado.jogador_acao = "idle"  # Voltar para o estado idle após o ataque

        estado.saude_inimigo -= dano
        estado.inimigo_acao = "Deceased_hurt" if dano > 0 else "Deceased_idle"
        mensagem = f"Você causou {dano} de dano!" if dano > 0 else mensagem
        dano_inimigo = True if dano > 0 else False

        screen.blit(background_batalha_img, (0, 0))
        desenhar_hud(screen, estado)
        desenhar_personagens(screen, jogador_animacoes, inimigo_animacoes, estado)
        desenhar_texto(mensagem, font, COLORS["BRANCO"], screen, 20, 20)
        desenhar_texto(f"Tempo de resposta: {tempo_resposta:.2f} segundos", font, COLORS["BRANCO"], screen, 20, 60)
        pygame.display.flip()
        pygame.time.delay(3000)

# Função para turno do inimigo
def turno_inimigo():
    global estado
    dano = random.randint(5, 15)
    tipo_acao = random.choice(["Ataque", "Magia", "Defesa"])
    dano_jogador = False
    mensagem = ""

    if tipo_acao == "Magia" and estado.mana_inimigo >= 10:
        estado.mana_inimigo -= 10
        dano += 5
    elif tipo_acao == "Defesa":
        estado.defendendo = True
        mensagem = "O inimigo se preparou para a defesa!"
        dano = 0
    else:
        if estado.defendendo:
            dano //= 2
            estado.defendendo = False
            mensagem = "Defesa bem-sucedida! Dano reduzido!"
        else:
            mensagem = ""

    estado.saude_jogador -= dano
    estado.inimigo_acao = "Deceased_attack" if dano > 0 else "Deceased_idle"
    dano_jogador = True if dano > 0 else False

    screen.blit(background_batalha_img, (0, 0))
    desenhar_hud(screen, estado)
    desenhar_personagens(screen, jogador_animacoes, inimigo_animacoes, estado)
    desenhar_texto(f"O inimigo causou {dano} de dano!", font, COLORS["BRANCO"], screen, 20, 20)
    desenhar_texto(mensagem, font, COLORS["BRANCO"], screen, 20, 60)
    pygame.display.flip()
    pygame.time.delay(2000)

    if estado.saude_jogador <= 0:
        estado.inimigo_acao = "Deceased_death"
        estado.batalha_ativa = False

# Função para checar fim da batalha
def checar_fim_batalha():
    if estado.saude_jogador <= 0:
        estado.inimigo_acao = "Deceased_death"
        return "Derrota"
    elif estado.saude_inimigo <= 0:
        estado.inimigo_acao = "Deceased_death"
        return "Vitória"
    return None

# Função para exibir a tela inicial
async def tela_inicial():
    tocar_musica(MUSICAS["menu"])
    screen.blit(background_menu_img, (0, 0))
    desenhar_texto("A Saga do Conhecimento", font, COLORS["BRANCO"], screen, WIDTH // 2 - 150, HEIGHT // 2 - 100)
    opcoes_menu = ["Jogar", "Modo História", "Opções", "Tela Cheia", "Sair"]
    retangulos_menu = [desenhar_texto(opcao, font, COLORS["BRANCO"], screen, WIDTH // 2 - 50, HEIGHT // 2 + i * 50) for i, opcao in enumerate(opcoes_menu)]
    pygame.display.flip()

    jogando = False
    opcao_selecionada = 0

    while not jogando:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(retangulos_menu)
                elif evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(retangulos_menu)
                elif evento.key == pygame.K_RETURN:
                    if opcao_selecionada == 0:
                        jogando = True
                        await batalha()
                    elif opcao_selecionada == 1:
                        jogando = True
                        await modo_historia()
                    elif opcao_selecionada == 2:
                        selecionar_nivel_e_disciplina()
                    elif opcao_selecionada == 3:
                        definir_modo_jogo(True)
                        await tela_inicial()
                    elif opcao_selecionada == 4:
                        pygame.quit()
                        exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, ret in enumerate(retangulos_menu):
                    if ret.collidepoint(evento.pos):
                        if i == 0:
                            jogando = True
                            await batalha()
                        elif i == 1:
                            jogando = True
                            await modo_historia()
                        elif i == 2:
                            selecionar_nivel_e_disciplina()
                        elif i == 3:
                            definir_modo_jogo(True)
                            await tela_inicial()
                        elif i == 4:
                            pygame.quit()
                            exit()
        for i, ret in enumerate(retangulos_menu):
            if ret.collidepoint(mouse_pos):
                opcao_selecionada = i
        screen.blit(background_menu_img, (0, 0))
        for i, opcao in enumerate(opcoes_menu):
            cor = COLORS["PRETO"] if i == opcao_selecionada else COLORS["BRANCO"]
            if i == opcao_selecionada:
                pygame.draw.rect(screen, COLORS["AMARELO"], retangulos_menu[i])
            desenhar_texto(opcao, font, cor, screen, WIDTH // 2 - 50, HEIGHT // 2 + i * 50)
        pygame.display.flip()
        await asyncio.sleep(0)

# Função para definir o modo de jogo
def definir_modo_jogo(tela_cheia):
    global screen, background_batalha_img, background_menu_img
    if tela_cheia:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background_batalha_img = carregar_imagem("background_batalha.png", WIDTH, HEIGHT)
    background_menu_img = carregar_imagem("background_menu.png", WIDTH, HEIGHT)

# Função principal do modo história
async def modo_historia():
    tocar_musica(MUSICAS["historia"])
    await fase_zero()
    await fase_um()

# Função para a fase zero do modo história
async def fase_zero():
    global estado
    running = True
    clock = pygame.time.Clock()
    jogador_pos = [100, HEIGHT - 120]
    jogador_vel_y = 0
    jogador_no_chao = True
    altura_chao = HEIGHT - 400

    estado.jogador_acao = "idle"
    estado.jogador_frame_atual = 0
    estado.jogador_frame_tempo = 0

    ret_sair = desenhar_texto("Sair", font, COLORS["BRANCO"], screen, WIDTH - 100, HEIGHT - 50)

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    running = False
                    await tela_inicial()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ret_sair.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    await tela_inicial()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            estado.jogador_acao = "run"
        else:
            estado.jogador_acao = "idle"

        if keys[pygame.K_LEFT]:
            jogador_pos[0] -= 5
        if keys[pygame.K_RIGHT]:
            jogador_pos[0] += 5
        if keys[pygame.K_SPACE] and jogador_no_chao:
            jogador_vel_y = -15
            jogador_no_chao = False

        jogador_vel_y += 1
        jogador_pos[1] += jogador_vel_y
        if jogador_pos[1] >= altura_chao:
            jogador_pos[1] = altura_chao
            jogador_vel_y = 0
            jogador_no_chao = True

        # Atualizar a animação do jogador
        estado.jogador_frame_tempo += 1
        if estado.jogador_frame_tempo >= 10:  # Ajuste o valor conforme necessário
            estado.jogador_frame_tempo = 0
            estado.jogador_frame_atual = (estado.jogador_frame_atual + 1) % len(jogador_animacoes[estado.jogador_acao])

        screen.blit(background_historia_img, (0, 0))
        if estado.jogador_frame_atual < len(jogador_animacoes[estado.jogador_acao]):
            screen.blit(jogador_animacoes[estado.jogador_acao][estado.jogador_frame_atual], jogador_pos)
        
        mouse_pos = pygame.mouse.get_pos()
        cor = COLORS["PRETO"] if ret_sair.collidepoint(mouse_pos) else COLORS["BRANCO"]
        if ret_sair.collidepoint(mouse_pos):
            pygame.draw.rect(screen, COLORS["AMARELO"], ret_sair)
        ret_sair = desenhar_texto("Sair", font, cor, screen, WIDTH - 100, HEIGHT - 50)
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

# Função para a fase um do modo história
async def fase_um():
    global estado
    running = True
    clock = pygame.time.Clock()
    jogador_pos = [100, HEIGHT - 120]
    jogador_vel_y = 0
    jogador_no_chao = True
    altura_chao = HEIGHT - 400

    estado.jogador_acao = "idle"
    estado.jogador_frame_atual = 0
    estado.jogador_frame_tempo = 0

    ret_sair = desenhar_texto("Sair", font, COLORS["BRANCO"], screen, WIDTH - 100, HEIGHT - 50)

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    running = False
                    await tela_inicial()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ret_sair.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    await tela_inicial()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            estado.jogador_acao = "run"
        else:
            estado.jogador_acao = "idle"

        if keys[pygame.K_LEFT]:
            jogador_pos[0] -= 5
        if keys[pygame.K_RIGHT]:
            jogador_pos[0] += 5
        if keys[pygame.K_SPACE] and jogador_no_chao:
            jogador_vel_y = -15
            jogador_no_chao = False

        jogador_vel_y += 1
        jogador_pos[1] += jogador_vel_y
        if jogador_pos[1] >= altura_chao:
            jogador_pos[1] = altura_chao
            jogador_vel_y = 0
            jogador_no_chao = True

        # Atualizar a animação do jogador
        estado.jogador_frame_tempo += 1
        if estado.jogador_frame_tempo >= 10:  # Ajuste o valor conforme necessário
            estado.jogador_frame_tempo = 0
            estado.jogador_frame_atual = (estado.jogador_frame_atual + 1) % len(jogador_animacoes[estado.jogador_acao])

        screen.blit(background_historia_img, (0, 0))
        if estado.jogador_frame_atual < len(jogador_animacoes[estado.jogador_acao]):
            screen.blit(jogador_animacoes[estado.jogador_acao][estado.jogador_frame_atual], jogador_pos)
        
        mouse_pos = pygame.mouse.get_pos()
        cor = COLORS["PRETO"] if ret_sair.collidepoint(mouse_pos) else COLORS["BRANCO"]
        if ret_sair.collidepoint(mouse_pos):
            pygame.draw.rect(screen, COLORS["AMARELO"], ret_sair)
        ret_sair = desenhar_texto("Sair", font, cor, screen, WIDTH - 100, HEIGHT - 50)
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

# Função para efeito de flash na tela
def flash_effect(screen, color, duration):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(color)
    screen.blit(overlay, (0, 0))
    pygame.display.flip()
    pygame.time.delay(duration)

# Inicializar o jogo
async def main():
    await tela_inicial()
    pygame.quit()

asyncio.run(main())
