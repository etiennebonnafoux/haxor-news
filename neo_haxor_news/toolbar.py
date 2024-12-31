from pygments.token import Token


class Toolbar(object):
    """Show information about the aws-shell in a tool bar.

    :type handler: callable
    :param handler: Wraps the callable `get_toolbar_items`.
    """

    def __init__(self, paginate_comments_cfg):
        self.handler = self._create_toolbar_handler(paginate_comments_cfg)

    def _create_toolbar_handler(self, paginate_comments_cfg):
        """Create the toolbar handler.

        :type paginate_comments_cfg: callable
        :param paginate_comments_cfg: Specifies whether to paginate comments.

        :rtype: callable
        :returns: get_toolbar_items.
        """
        assert callable(paginate_comments_cfg)

        def get_toolbar_items(_):
            """Return the toolbar items.

            :type _: :class:`prompt_toolkit.Cli`
            :param _: (Unused)

            :rtype: list
            :return: A list of (pygments.Token.Toolbar, str).
            """
            # if paginate_comments_cfg():
            #     paginate_comments_token = Token.Toolbar.On
            #     paginate_comments = 'ON'
            # else:
            #     paginate_comments_token = Token.Toolbar.Off
            #     paginate_comments = 'OFF'
            return [
                # (paginate_comments_token,
                #  ' [F2] Paginate Comments: {0} '.format(paginate_comments)),
                (Token.Toolbar, " [F10] Exit ")
            ]

        return get_toolbar_items
