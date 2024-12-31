from pygments.util import ClassNotFound
from prompt_toolkit.styles import Style
import pygments.styles


class StyleFactory:
    """Provide styles for the autocomplete menu and the toolbar.

    :type style: :class:`pygments.style.StyleMeta`
    :param style: An instance of `pygments.style.StyleMeta`.
    """

    def __init__(self, name):
        self.style = self.style_factory(name)

    def style_factory(self, name):
        """Retrieve the specified pygments style.

        If the specified style is not found, the vim style is returned.

        :type style_name: str
        :param style_name: The pygments style name.

        :rtype: :class:`pygments.style.StyleMeta`
        :return: An instance of `pygments.style.StyleMeta`.
        """
        try:
            style = pygments.styles.get_style_by_name(name)
        except ClassNotFound:
            style = pygments.styles.get_style_by_name("native")

        # Create styles dictionary.
        styles = {}
        styles.update(style.styles)
        custom_styles = {
            # Completion menu styles
            'completion-menu.completion.current': 'bg:#00aaaa #000000',
            'completion-menu.completion': 'bg:#008888 #ffffff',
            'completion-menu.meta.completion.current': 'bg:#00aaaa #000000',
            'completion-menu.meta.completion': 'bg:#00aaaa #ffffff',
            'completion-menu.progress-button': 'bg:#003333',
            'completion-menu.progress-bar': 'bg:#00aaaa',
            
            # Scrollbar styles
            'scrollbar': 'bg:#00aaaa',
            'scrollbar.button': 'bg:#003333',
            
            # Toolbar styles
            'bottom-toolbar': 'bg:#222222 #cccccc',
            'bottom-toolbar.off': 'bg:#222222 #696969',
            'bottom-toolbar.on': 'bg:#222222 #ffffff',
            'bottom-toolbar.search': 'bold',
            'bottom-toolbar.search.text': 'noinherit nobold',
            'bottom-toolbar.system': 'bold',
            'bottom-toolbar.arg': 'bold',
            'bottom-toolbar.arg.text': 'noinherit nobold',
        }

        return Style.from_dict(custom_styles)
