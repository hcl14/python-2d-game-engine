from constants import FONT
from constants import NATIVE_RECT
from constants import NATIVE_SURF
from constants import pg
from nodes.curtain import Curtain
from typeguard import typechecked


@typechecked
class Button:
    """
    Needs to be inside a button container

    Always need a description
    """

    BUTTON_INACTIVE_BODY_COLOR: str = "#000f28"
    BUTTON_INACTIVE_LINE_COLOR: str = "#004a89"
    BUTTON_INACTIVE_TEXT_COLOR: str = "#bac3d2"

    BUTTON_ACTIVE_BODY_COLOR: str = "#126a9c"
    BUTTON_ACTIVE_LINE_COLOR: str = "#1896ea"
    BUTTON_ACTIVE_TEXT_COLOR: str = "#feffff"

    DESCRIPTION_TEXT_BOTTOM_PADDING: int = 2

    INACTIVE: int = 0
    ACTIVE: int = 1

    def __init__(
        self,
        width: int,
        height: int,
        topleft: tuple[int, int],
        text: str,
        text_topleft: tuple[int, int],
        description_text: str,
    ):
        self.width: int = width

        self.height: int = height

        self.surf: pg.Surface = pg.Surface((self.width, self.height))

        self.surf.fill(self.BUTTON_INACTIVE_BODY_COLOR)

        pg.draw.line(
            self.surf,
            self.BUTTON_INACTIVE_LINE_COLOR,
            (0, 0),
            (0, self.height),
        )

        self.rect: pg.Rect = self.surf.get_rect()

        self.rect.topleft = topleft

        self.text: str = text

        self.text_top_left: tuple[int, int] = text_topleft

        pg.draw.line(
            self.surf,
            self.BUTTON_INACTIVE_LINE_COLOR,
            (0, 0),
            (0, self.height),
        )

        FONT.render_to(
            self.surf,
            self.text_top_left,
            self.text,
            self.BUTTON_INACTIVE_TEXT_COLOR,
        )

        self.active_curtain_surf: pg.Surface = pg.Surface(
            (self.width + 1, self.height)  # shift to left
        )

        self.active_curtain_duration: float = 300.0
        self.active_curtain_start: int = Curtain.INVISIBLE
        self.active_curtain_max_alpha: int = 225
        self.active_curtain_is_invisible: bool = True
        self.active_curtain: Curtain = Curtain(
            self.active_curtain_duration,
            self.active_curtain_start,
            self.active_curtain_max_alpha,
            self.active_curtain_surf,
            self.active_curtain_is_invisible,
        )
        self.active_curtain.rect.topright = self.rect.topright

        self.active_surf: pg.Surface = pg.Surface(
            (self.width + 1, self.height)  # shift to left
        )

        self.active_surf.fill(self.BUTTON_ACTIVE_BODY_COLOR)

        pg.draw.line(
            self.active_surf,
            self.BUTTON_ACTIVE_TEXT_COLOR,
            (0, 0),
            (0, self.height),
        )

        pg.draw.line(
            self.active_surf,
            self.BUTTON_ACTIVE_LINE_COLOR,
            (1, 0),
            (1, self.height),
        )

        FONT.render_to(
            self.active_surf,
            self.text_top_left,
            self.text,
            self.BUTTON_ACTIVE_TEXT_COLOR,
        )

        self.active_curtain.surf.blit(self.active_surf, (0, 0))

        self.description_text: str = description_text

        self.description_text_rect: pg.Rect = FONT.get_rect(
            self.description_text
        )
        self.description_text_rect.center = NATIVE_RECT.center
        self.description_text_rect.bottom = NATIVE_RECT.bottom
        self.description_text_rect.y -= self.DESCRIPTION_TEXT_BOTTOM_PADDING

        self.initial_state: int = self.INACTIVE

        self.state: int = self.initial_state

        self.init_state()

    def init_state(self) -> None:
        """
        This is set state for none to initial state.
        """
        NATIVE_SURF.blit(self.surf, self.rect)

    def update(self, dt: int) -> None:
        self.active_curtain.update(dt)

    def draw(self, surf: pg.Surface, y_offset: int) -> None:
        # Draw my description if I am active
        if self.state == self.ACTIVE:
            FONT.render_to(
                surf,
                self.description_text_rect,
                self.description_text,
                self.BUTTON_ACTIVE_TEXT_COLOR,
            )
        surf.blit(self.surf, (self.rect.x, self.rect.y + y_offset))
        self.active_curtain.draw(surf, y_offset)

    def set_state(self, value: int) -> None:
        old_state: int = self.state
        self.state = value

        if old_state == self.INACTIVE:
            if self.state == self.ACTIVE:
                self.active_curtain.go_to_opaque()

        elif old_state == self.ACTIVE:
            if self.state == self.INACTIVE:
                self.active_curtain.go_to_invisible()
