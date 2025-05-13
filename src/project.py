import pygame
import sys
from graph import DialogGraph, DialogNode, DialogChoice
from text_util import layout_text_in_area

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pumpkin")

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
            DialogNode("START", "You just got home after class. You start to walk to your bedroom...", [
                DialogChoice("Enter the room", "BEDROOM"),
                DialogChoice("Call out for your cat", "APARTMENT")
            ]),
            DialogNode("APARTMENT", "No response. Everything is quiet", [
                DialogChoice("Enter the room", "BEDROOM")
            ]),
            DialogNode("BEDROOM", "Your room is clean, aside from the coffee cups and miscellaneous papers cluttering the desk", [
                DialogChoice("Look under the bed", "CAT_FOUND"),
                DialogChoice("Check the window sill", "WINDOW")
            ]),
            DialogNode("WINDOW", "You walk over to the window sill. The sunlight is warm, but nothing's there", [
                DialogChoice("Look under the bed", "CAT_FOUND"),
                DialogChoice("Leave the room", "START")
            ]),
            DialogNode("CAT_FOUND", "You peek under the bed and find a sleepy orange cat staring back at you!", [
                DialogChoice("Have a staring contest", "NUETRAL_END"),
                DialogChoice("Sit and pet the cat", "HAPPY_END")
            ]),
            DialogNode("NUETRAL_END", "The cat stares at you with wide, unblinking eyes. The room feels colder now. You slowly back away, unsure why you feel watched, even after you leave.", [
                DialogChoice("Start over", "START"),
                DialogChoice("Exit", "EXIT")
            ]),     
            DialogNode("HAPPY_END", "You sit quietly, petting Pumpkin as she purrs happily. A perfect moment.", [
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