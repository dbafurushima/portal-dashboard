# https://github.com/aws/aws-cli/blob/develop/awscli/help.py
import os

from .argparser import ArgTableArgParser


class HelpCommand(object):
    """
    HelpCommand Interface
    ---------------------
    A HelpCommand object acts as the interface between objects in the
    CLI (e.g. Providers, Services, Operations, etc.) and the documentation
    system (bcdoc).

    A HelpCommand object wraps the object from the CLI space and provides
    a consistent interface to critical information needed by the
    documentation pipeline such as the object's name, description, etc.

    The HelpCommand object is passed to the component of the
    documentation pipeline that fires documentation events.  It is
    then passed on to each document event handler that has registered
    for the events.

    All HelpCommand objects contain the following attributes:

        + ``obj`` - The object that is being documented.
        + ``command_table`` - A dict mapping command names to
              callable objects.
        + ``arg_table`` - A dict mapping argument names to callable objects.
        + ``doc`` - A ``Document`` object that is used to collect the
              generated documentation.

    In addition, please note the `properties` defined below which are
    required to allow the object to be used in the document pipeline.

    Implementations of HelpCommand are provided here for Provider,
    Service and Operation objects.  Other implementations for other
    types of objects might be needed for customization in plugins.
    As long as the implementations conform to this basic interface
    it should be possible to pass them to the documentation system
    and generate interactive and static help files.
    """

    EventHandlerClass = None
    """
    Each subclass should define this class variable to point to the
    EventHandler class used by this HelpCommand.
    """

    def __init__(self, obj, command_table, arg_table):
        self.obj = obj
        if command_table is None:
            command_table = {}
        self.command_table = command_table
        if arg_table is None:
            arg_table = {}
        self.arg_table = arg_table
        self._subcommand_table = {}
        self._related_items = []

    @property
    def event_class(self):
        """
        Return the ``event_class`` for this object.

        The ``event_class`` is used by the documentation pipeline
        when generating documentation events.  For the event below::

            doc-title.<event_class>.<name>

        The document pipeline would use this property to determine
        the ``event_class`` value.
        """
        pass

    @property
    def name(self):
        """
        Return the name of the wrapped object.

        This would be called by the document pipeline to determine
        the ``name`` to be inserted into the event, as shown above.
        """
        pass

    @property
    def subcommand_table(self):
        """These are the commands that may follow after the help command"""
        return self._subcommand_table

    @property
    def related_items(self):
        """This is list of items that are related to the help command"""
        return self._related_items

    def __call__(self, args, parsed_globals):
        if args:
            subcommand_parser = ArgTableArgParser({}, self.subcommand_table)
            parsed, remaining = subcommand_parser.parse_known_args(args)
            if getattr(parsed, 'subcommand', None) is not None:
                return self.subcommand_table[parsed.subcommand](remaining,
                                                                parsed_globals)

        # Create an event handler for a Provider Document
        # instance = self.EventHandlerClass(self)
        # Now generate all of the events for a Provider document.
        # We pass ourselves along so that we can, in turn, get passed
        # to all event handlers.
        # self.renderer.render(self.doc.getvalue())
        # instance.unregister()
        # TODO HELP
