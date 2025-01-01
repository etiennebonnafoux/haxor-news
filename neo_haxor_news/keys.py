from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from collections.abc import Callable
from prompt_toolkit.key_binding.key_processor import KeyPressEvent


class KeyManager:
    """A custom :class:`prompt_toolkit.KeyBindingManager`.

    Handle togging of:
        * Comment pagination.

    :type manager: :class:`prompt_toolkit.key_binding.manager.
        KeyBindingManager`
    :param manager: An instance of `prompt_toolkit.key_binding.manager.
        KeyBindingManager`.
    """

    def __init__(
        self, set_paginate_comments: Callable, get_paginate_comments: Callable
    ):
        self.manager: KeyBindings | None = None
        self._create_key_manager(set_paginate_comments, get_paginate_comments)

    def _create_key_manager(
        self, set_paginate_comments: Callable, get_paginate_comments: Callable
    ):
        """Create and initialize the keybinding manager.

        Args:
            set_paginate_comments (Callable): Sets the paginate comments config.
            get_paginate_comments (Callable): Gets the paginate comments config.

        """
        assert callable(set_paginate_comments)
        assert callable(get_paginate_comments)
        self.manager = KeyBindings()

        @self.manager.add(Keys.F2)
        def handle_f2(_):
            """Enable/Disable paginate comments mode.

            This method is currently disabled.

            Args:
                _ (_): Unused Event
            """
            # set_paginate_comments(not get_paginate_comments())
            pass

        @self.manager.add(Keys.F10)
        def handle_f10(_):
            """Quit when the `F10` key is pressed.

            Args:
                _ (_): The event unused

            Raises:
                EOFError: `EOFError` to quit the app.
            """
            raise EOFError

        @self.manager.add(Keys.ControlSpace)
        def handle_ctrl_space(event: KeyPressEvent):
            """Initialize autocompletion at the cursor.

            If the autocompletion menu is not showing, display it with the
            appropriate completions for the context.

            If the menu is showing, select the next completion.

            Args:
                event (KeyPressEvent): An instance of `KeyPressEvent`
            """
            b = event.current_buffer
            if b.complete_state:
                b.complete_next()
            else:
                b.start_completion(select_first=False)
