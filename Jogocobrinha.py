import pygame, sys, time, random

# Nível de dificuldade
# fácil      ->  10
# Médio      ->  25
# difícil    ->  40
# impossível ->  100
# Deus na causa ->  120
dificuldade = 25

# Tamanho da tela
largura = 720
altura = 480

# erros
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f' {check_errors[1]} ')
    sys.exit(-1)

# janela do jogo
pygame.display.set_caption('Jogo da cobrinha')
game_window = pygame.display.set_mode((largura, altura))

# corres (R, G, B)
preto = pygame.Color(0, 0, 0)
branco = pygame.Color(255, 255, 255)
vermelho = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
azul = pygame.Color(0, 0, 255)

# FPS
fps_controller = pygame.time.Clock()

# Variáveis do jogo
snake_pos = [100, 50]
snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

food_pos = [random.randrange(1, (largura // 10)) * 10, random.randrange(1, (altura // 10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# Fim de jogo
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('VOCÊ PERDEU', True, vermelho)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (largura / 2, altura / 4)
    game_window.fill(preto)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, vermelho, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Pontos
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Pontos : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (largura / 10, 15)
    else:
        score_rect.midtop = (largura / 2, altura / 1.25)
    game_window.blit(score_surface, score_rect)



# lógica
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'

            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # movendo a cobra
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # crescimento do corpo
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning da comida
    if not food_spawn:
        food_pos = [random.randrange(1, (largura // 10)) * 10, random.randrange(1, (altura // 10)) * 10]
    food_spawn = True

    game_window.fill(preto)
    for pos in snake_body:

        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # comida forma
    pygame.draw.rect(game_window, branco, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # fim de jogo
    if snake_pos[0] < 0 or snake_pos[0] > largura - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > altura - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, branco, 'console', 20)
    pygame.display.update()
    fps_controller.tick(dificuldade)
