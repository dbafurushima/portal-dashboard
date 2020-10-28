import logging
import os

SCALAR_TYPES = set([
    'string', 'float', 'integer', 'long', 'boolean', 'double',
    'blob', 'timestamp'
])
DOC_EVENTS = []

logger = logging.getLogger(__name__)


class CLIDocumentEventHandler(object):

    def __init__(self, help_command):
        self.help_command = help_command
        self._arg_groups = self._build_arg_table_groups(help_command)
        self._documented_arg_groups = []
        # print('CLIDocumentEventHandler.__init__(help_command).arg_table: %s' % help_command.arg_table)

    def _build_arg_table_groups(self, help_command):
        arg_groups = {}
        for name, arg in help_command.arg_table.items():
            if arg.group_name is not None:
                # print('CLIDocumentEventHandler._build_arg_table_groups().arg.group_name: %s' % arg.group_name)
                arg_groups.setdefault(arg.group_name, []).append(arg)
        return arg_groups

    def _get_argument_type_name(self, shape, default):
        # if is_json_value_header(shape):
        #     return 'JSON'
        return default

    # These are default doc handlers that apply in the general case.

    def _create_help(self, help_command, **kwargs):
        self.doc_title(help_command)

    def create_help(self, help_command):
        self._create_help(help_command)

    def doc_breadcrumbs(self, help_command, **kwargs):
        pass

    def doc_title(self, help_command, **kwargs):
        doc = help_command.doc
        doc.style.new_paragraph()
        reference = help_command.event_class.replace('.', ' ')
        if reference != 'mng':
            reference = 'mng ' + reference
        doc.writeln('.. _cli:%s:' % reference)
        doc.style.h1(help_command.name)

    def doc_description(self, help_command, **kwargs):
        pass

    def doc_synopsis_start(self, help_command, **kwargs):
        pass

    def doc_synopsis_option(self, arg_name, help_command, **kwargs):
        pass

    def doc_synopsis_end(self, help_command, **kwargs):
        pass

    def doc_options_start(self, help_command, **kwargs):
        pass

    def doc_option(self, arg_name, help_command, **kwargs):
        pass

    def doc_relateditems_start(self, help_command, **kwargs):
        pass
    def doc_relateditem(self, help_command, related_item, **kwargs):
        pass

    def _document_enums(self, model, doc):
        pass

    def _document_nested_structure(self, model, doc):
        """Recursively documents parameters in nested structures"""
        pass

    def _doc_member(self, doc, member_name, member_shape, stack):
        pass

    def _do_doc_member(self, doc, member_name, member_shape, stack):
        pass


class OperationDocumentEventHandler(CLIDocumentEventHandler):

    mng_DOC_BASE = ''

    def doc_description(self, help_command, **kwargs):
        doc = help_command.doc
        operation_model = help_command.obj
        doc.style.h2('Description')
        doc.include_doc_string(operation_model.documentation)
        self._add_webapi_crosslink(help_command)
        self._add_top_level_args_reference(help_command)

    def _add_top_level_args_reference(self, help_command):
        pass

    def _add_webapi_crosslink(self, help_command):
        pass

    def _json_example_value_name(self, argument_model, include_enum_values=True):
        pass

    def _json_example(self, doc, argument_model, stack):
        pass

    def _do_json_example(self, doc, argument_model, stack):
        pass

    def _doc_input_structure_members(self, doc, argument_model, stack):
        pass

    def doc_option_example(self, arg_name, help_command, event_name, **kwargs):
        pass

    def _write_valid_enums(self, doc, enum_values):
        pass

    def doc_output(self, help_command, event_name, **kwargs):
        pass

    def doc_options_end(self, help_command, **kwargs):
        pass
