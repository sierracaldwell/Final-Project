import pygame
import sys
from graph import DialogGraph, DialogNode, DialogChoice
from text_util import layout_text_in_area

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sunborne")

# Colors and fonts
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
FONT = pygame.font.SysFont("arial", 24)
LINE_HEIGHT = FONT.get_linesize()

clock = pygame.time.Clock()

def draw_text_box(text, y_start, width):
    lines = layout_text_in_area(text, lambda t: FONT.size(t)[0], width)
    y = y_start
    for line in lines:
        rendered = FONT.render(line, True, WHITE)
        screen.blit(rendered, (40, y))
        y += LINE_HEIGHT + 5
    return y

def draw_choices(choices, y_start, selected_button=None):
    buttons = []
    for i, choice in enumerate(choices):
        rect = pygame.Rect(40, y_start + i * 100, 700, 90)
        buttons.append((rect, choice.text))

        # Button fill color
        fill_color = GRAY if selected_button == i else BLACK

        # Draw button background
        pygame.draw.rect(screen, fill_color, rect)
        pygame.draw.rect(screen, WHITE, rect, 2)

        # Draw image if it exists
        if choice.image_path:
            try:
                image = pygame.image.load(choice.image_path)
                image = pygame.transform.scale(image, (80, 80))  # Resize if needed
                screen.blit(image, (rect.x + 10, rect.y + 5))
                text_offset = 100  # Shift text to the right of image
            except pygame.error:
                text_offset = 10  # If loading fails, fallback to normal text position
        else:
            text_offset = 10

        # Draw text
        label = FONT.render(choice.text, True, WHITE)
        screen.blit(label, (rect.x + text_offset, rect.y + 30))

    return buttons

def render_node(node, selected_button=None):
    screen.fill(BLACK)
    y = draw_text_box(node.text, 40, WIDTH - 80)
    buttons = draw_choices(node.choices, y + 20, selected_button)
    pygame.display.flip()
    return buttons

def main():
    dialog_graph = DialogGraph(
        root_node_id="START",
        nodes=[
            DialogNode("START", "You're in a dimly lit room. There are two doors...", [
                DialogChoice("Exit west", "WEST", "assets/west_door.png"),
                DialogChoice("Exit east", "EAST", "assets/east_door.png")
            ]),
            DialogNode("WEST", "You're in a library. Nothing of interest.", [
                DialogChoice("Leave the library", "START")
            ]),
            DialogNode("EAST", "You're in a corridor. There's a hole!", [
                DialogChoice("Go back", "START"),
                DialogChoice("Jump in", "BASEMENT")
            ]),
            DialogNode("BASEMENT", "You fall hard into a dark cellar.", [
                DialogChoice("Sit and wait", "SUNLIGHT"),
                DialogChoice("Feel your way", "SPEAR")
            ]),
            DialogNode("SUNLIGHT", "Light enters. You see spears. Lucky you waited!", [
                DialogChoice("Leave", "VICTORY")
            ]),
            DialogNode("SPEAR", "You walk into a spear. You are dead.", [
                DialogChoice("Retry", "START"),
                DialogChoice("Exit", "EXIT")
            ]),
            DialogNode("VICTORY", "You escaped!", [
                DialogChoice("Start again", "START"),
                DialogChoice("Exit", "EXIT")
            ]),
            DialogNode("EXIT", "", [])
        ]
    )

    running = True
    selected = None
    buttons = []
    current_node = dialog_graph.current_node()

    while running:
        clock.tick(30)
        mouse_pos = pygame.mouse.get_pos()

        if current_node.node_id == "EXIT":
            running = False
            continue

        # Hover detection
        selected = None
        buttons = render_node(current_node)
        for i, (rect, _) in enumerate(buttons):
            if rect.collidepoint(mouse_pos):
                selected = i
                break

        # Render again with highlight
        buttons = render_node(current_node, selected)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and selected is not None:
                dialog_graph.make_choice(selected)
                current_node = dialog_graph.current_node()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()