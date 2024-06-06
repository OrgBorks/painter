import pygame

pygame.init()

screen_height = 1920
screen_width = 1080
#! useful flags: pygame.FULLSCREEN, pygame.RESIZABLE, pygame.NOFRAME, pygame.SCALED, pygame.SHOWN, pygame.HIDDEN
screen = pygame.display.set_mode((screen_height, screen_width))
clock = pygame.time.Clock()
dt = 0
running = True

#! other useful things
#! pygame.display.get_active()
#! pygame.display.get_desktop_sizes() -> find suitable sizes for non-fullscreen
#! pygame.display.list_modes() -> find suitable sizes for fullscreen
#! pygame.display.set_caption("my name jeff")
#! pygame.display.iconify()
#! pygame.display.toggle_fullscreen()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #! other events
        #! KEYDOWN (key, mod, unicode, scancode)
        #! KEYUP (~)
        #! MOUSEMOTION (pos, rel, buttons, touch)
        #! MOUSEBUTTONUP (pos, button, touch)
        #! MOUSEBUTTONDOWN (~)

        #! window events
        #! ALL HAVE PREFIX "WINDOW"
        #! SHOWN, HIDDEN, EXPOSED, MOVED, RESIZED, SIZECHANGED, MINIMIZED, MAXIMIZED,
        #! RESTORED, ENTER, LEAVE, FOCUSGAINED/LOST, CLOSE, DISPLAYCHANGED

        #! sample code for text input
    #     if event.type == pygame.KEYDOWN:
    #         # check backspace
    #         if event.key == pygame.K_BACKSPACE and blanks_text:
    #             blanks_text = blanks_text[:-1]
    #             backspace = True
    #             backspace_start = time.time()
    #         if event.key == pygame.K_RETURN and blanks_text:
    #             blanks_storage.append(blanks_text)
    #             blanks_text = ""
    #             i += 1
    #     if event.type == pygame.KEYUP:
    #         if event.key == pygame.K_BACKSPACE:
    #             backspace = False
    #             backspace_start = None
    #     if event.type == pygame.TEXTINPUT:
    #         blanks_text += event.text
    #
    # if backspace and time.time() - backspace_start > 0.5:
    #     if backspace_rapid and time.time() - backspace_rapid > 0.05:
    #         blanks_text = blanks_text[:-1]
    #         backspace_rapid = time.time()
    #     elif not backspace_rapid:
    #         backspace_rapid = time.time()

    #! rest of loop code here
