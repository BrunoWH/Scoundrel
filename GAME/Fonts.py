import pygame
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Font Viewer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Get fonts and sort alphabetically
fonts = pygame.font.get_fonts()
fonts.sort()

# Layout settings
FONT_SIZE = 24
LINE_HEIGHT = 30
MARGIN_TOP = 20
MARGIN_LEFT = 20

# Calculate how many lines fit per page
lines_per_page = (HEIGHT - 100) // LINE_HEIGHT  # leave space for buttons

# Pagination
pages = [
    fonts[i:i + lines_per_page]
    for i in range(0, len(fonts), lines_per_page)
]
current_page = 0

# Button setup
button_font = pygame.font.SysFont(None, 30)

left_button = pygame.Rect(50, HEIGHT - 60, 100, 40)
right_button = pygame.Rect(WIDTH - 150, HEIGHT - 60, 100, 40)


def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_buttons():
    pygame.draw.rect(screen, GRAY, left_button)
    pygame.draw.rect(screen, GRAY, right_button)

    draw_text("Left", button_font, BLACK, left_button.x + 25, left_button.y + 10)
    draw_text("Right", button_font, BLACK, right_button.x + 20, right_button.y + 10)


def draw_page():
    y = MARGIN_TOP

    for font_name in pages[current_page]:
        try:
            font = pygame.font.SysFont(font_name, FONT_SIZE)
        except:
            font = pygame.font.Font(None, FONT_SIZE)

        text = f"-{font_name}: Example"
        draw_text(text, font, BLACK, MARGIN_LEFT, y)
        y += LINE_HEIGHT

    # Page indicator
    page_text = f"Page {current_page + 1}/{len(pages)}"
    draw_text(page_text, button_font, BLACK, WIDTH // 2 - 50, HEIGHT - 50)


# Main loop
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if left_button.collidepoint(event.pos):
                if current_page > 0:
                    current_page -= 1

            if right_button.collidepoint(event.pos):
                if current_page < len(pages) - 1:
                    current_page += 1

        # Optional: keyboard navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and current_page > 0:
                current_page -= 1
            if event.key == pygame.K_RIGHT and current_page < len(pages) - 1:
                current_page += 1

    draw_page()
    draw_buttons()

    pygame.display.flip()
    clock.tick(60)