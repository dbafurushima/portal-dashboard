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

    def _build_arg_table_groups(self, help_command):
        arg_groups = {}
        for name, arg in help_command.arg_table.items():
            if arg.group_name is not None:
                arg_groups.setdefault(arg.group_name, []).append(arg)
        return arg_groups

    def _get_argument_type_name(self, shape, default):
        # if is_json_value_header(shape):
        #     return 'JSON'
        return default

    # These are default doc handlers that apply in the general case.

    def doc_breadcrumbs(self, help_command, **kwargs):
        doc = help_command.doc
        if doc.target != 'man':
            cmd_names = help_command.event_class.split('.')
            doc.write('[ ')
            doc.write(':ref:`aws <cli:aws>`')
            full_cmd_list = ['aws']
            for cmd in cmd_names[:-1]:
                doc.write(' . ')
                full_cmd_list.append(cmd)
                full_cmd_name = ' '.join(full_cmd_list)
                doc.write(':ref:`%s <cli:%s>`' % (cmd, full_cmd_name))
            doc.write(' ]')

    def doc_title(self, help_command, **kwargs):
        doc = help_command.doc
        doc.style.new_paragraph()
        reference = help_command.event_class.replace('.', ' ')
        if reference != 'aws':
            reference = 'aws ' + reference
        doc.writeln('.. _cli:%s:' % reference)
        doc.style.h1(help_command.name)

    def doc_description(self, help_command, **kwargs):
        doc = help_command.doc
        doc.style.h2('Description')
        doc.include_doc_string(help_command.description)
        doc.style.new_paragraph()

    def doc_synopsis_start(self, help_command, **kwargs):
        self._documented_arg_groups = []
        doc = help_command.doc
        doc.style.h2('Synopsis')
        doc.style.start_codeblock()
        doc.writeln('%s' % help_command.name)

    def doc_synopsis_option(self, arg_name, help_command, **kwargs):
        doc = help_command.doc
        argument = help_command.arg_table[arg_name]
        if argument.group_name in self._arg_groups:
            if argument.group_name in self._documented_arg_groups:
                # This arg is already documented so we can move on.
                return
            option_str = ' | '.join(
                [a.cli_name for a in
                 self._arg_groups[argument.group_name]])
            self._documented_arg_groups.append(argument.group_name)
        elif argument.cli_name.startswith('--'):
            option_str = '%s <value>' % argument.cli_name
        else:
            option_str = '<%s>' % argument.cli_name
        if not (argument.required
                or getattr(argument, '_DOCUMENT_AS_REQUIRED', False)):
            option_str = '[%s]' % option_str
        doc.writeln('%s' % option_str)

    def doc_synopsis_end(self, help_command, **kwargs):
        doc = help_command.doc
        doc.style.end_codeblock()
        # Reset the documented arg groups for other sections
        # that may document args (the detailed docs following
        # the synopsis).
        self._documented_arg_groups = []

    def doc_options_start(self, help_command, **kwargs):
        doc = help_command.doc
        doc.style.h2('Options')
        if not help_command.arg_table:
            doc.write('*None*\n')

    def doc_option(self, arg_name, help_command, **kwargs):
        doc = help_command.doc
        argument = help_command.arg_table[arg_name]
        if argument.group_name in self._arg_groups:
            if argument.group_name in self._documented_arg_groups:
                # This arg is already documented so we can move on.
                return
            name = ' | '.join(
                ['``%s``' % a.cli_name for a in
                 self._arg_groups[argument.group_name]])
            self._documented_arg_groups.append(argument.group_name)
        else:
            name = '``%s``' % argument.cli_name
        doc.write('%s (%s)\n' % (name, self._get_argument_type_name(
            argument.argument_model, argument.cli_type_name)))
        doc.style.indent()
        doc.include_doc_string(argument.documentation)
        if hasattr(argument, 'argument_model'):
            self._document_enums(argument.argument_model, doc)
            self._document_nested_structure(argument.argument_model, doc)
        doc.style.dedent()
        doc.style.new_paragraph()

    def doc_relateditems_start(self, help_command, **kwargs):
        if help_command.related_items:
            doc = help_command.doc
            doc.style.h2('See Also')

    def doc_relateditem(self, help_command, related_item, **kwargs):
        doc = help_command.doc
        doc.write('* ')
        doc.style.sphinx_reference_label(
            label='cli:%s' % related_item,
            text=related_item
        )
        doc.write('\n')

    def _document_enums(self, model, doc):
        """Documents top-level parameter enums"""
        """
        if isinstance(model, StringShape):
            if model.enum:
                doc.style.new_paragraph()
                doc.write('Possible values:')
                doc.style.start_ul()
                for enum in model.enum:
                    doc.style.li('``%s``' % enum)
                doc.style.end_ul()
        """
        pass

    def _document_nested_structure(self, model, doc):
        """Recursively documents parameters in nested structures"""
        member_type_name = getattr(model, 'type_name', None)
        if member_type_name == 'structure':
            for member_name, member_shape in model.members.items():
                self._doc_member(doc, member_name, member_shape,
                                 stack=[model.name])
        elif member_type_name == 'list':
            self._doc_member(doc, '', model.member, stack=[model.name])
        elif member_type_name == 'map':
            key_shape = model.key
            key_name = key_shape.serialization.get('name', 'key')
            self._doc_member(doc, key_name, key_shape, stack=[model.name])
            value_shape = model.value
            value_name = value_shape.serialization.get('name', 'value')
            self._doc_member(doc, value_name, value_shape, stack=[model.name])

    def _doc_member(self, doc, member_name, member_shape, stack):
        if member_shape.name in stack:
            # Document the recursion once, otherwise just
            # note the fact that it's recursive and return.
            if stack.count(member_shape.name) > 1:
                if member_shape.type_name == 'structure':
                    doc.write('( ... recursive ... )')
                return
        stack.append(member_shape.name)
        try:
            self._do_doc_member(doc, member_name,
                                member_shape, stack)
        finally:
            stack.pop()

    def _do_doc_member(self, doc, member_name, member_shape, stack):
        docs = member_shape.documentation
        if member_name:
            doc.write('%s -> (%s)' % (member_name, self._get_argument_type_name(
                                      member_shape, member_shape.type_name)))
        else:
            doc.write('(%s)' % member_shape.type_name)
        doc.style.indent()
        doc.style.new_paragraph()
        doc.include_doc_string(docs)
        doc.style.new_paragraph()
        member_type_name = member_shape.type_name
        if member_type_name == 'structure':
            for sub_name, sub_shape in member_shape.members.items():
                self._doc_member(doc, sub_name, sub_shape, stack)
        elif member_type_name == 'map':
            key_shape = member_shape.key
            key_name = key_shape.serialization.get('name', 'key')
            self._doc_member(doc, key_name, key_shape, stack)
            value_shape = member_shape.value
            value_name = value_shape.serialization.get('name', 'value')
            self._doc_member(doc, value_name, value_shape, stack)
        elif member_type_name == 'list':
            self._doc_member(doc, '', member_shape.member, stack)
        doc.style.dedent()
        doc.style.new_paragraph()


class ProviderDocumentEventHandler(CLIDocumentEventHandler):

    def doc_breadcrumbs(self, help_command, event_name, **kwargs):
        pass

    def doc_synopsis_start(self, help_command, **kwargs):
        doc = help_command.doc
        doc.style.h2('Synopsis')
        doc.style.codeblock(help_command.synopsis)
        doc.include_doc_string(help_command.help_usage)

    def doc_synopsis_option(self, arg_name, help_command, **kwargs):
        pass

    def doc_synopsis_end(self, help_command, **kwargs):
        doc = help_command.doc
        doc.style.new_paragraph()

    def doc_options_start(self, help_command, **kwargs):
        doc = help_command.doc
        doc.style.h2('Options')

    def doc_option(self, arg_name, help_command, **kwargs):
        doc = help_command.doc
        argument = help_command.arg_table[arg_name]
        doc.writeln('``%s`` (%s)' % (argument.cli_name,
                                     argument.cli_type_name))
        doc.include_doc_string(argument.documentation)
        if argument.choices:
            doc.style.start_ul()
            for choice in argument.choices:
                doc.style.li(choice)
            doc.style.end_ul()

    def doc_subitems_start(self, help_command, **kwargs):
        doc = help_command.doc
        doc.style.h2('Available Services')
        doc.style.toctree()

    def doc_subitem(self, command_name, help_command, **kwargs):
        doc = help_command.doc
        file_name = '%s/index' % command_name
        doc.style.tocitem(command_name, file_name=file_name)


class ServiceDocumentEventHandler(CLIDocumentEventHandler):

    # A service document has no synopsis.
    def doc_synopsis_start(self, help_command, **kwargs):
        pass

    def doc_synopsis_option(self, arg_name, help_command, **kwargs):
        pass

    def doc_synopsis_end(self, help_command, **kwargs):
        pass

    # A service document has no option section.
    def doc_options_start(self, help_command, **kwargs):
        pass

    def doc_option(self, arg_name, help_command, **kwargs):
        pass

    def doc_option_example(self, arg_name, help_command, **kwargs):
        pass

    def doc_options_end(self, help_command, **kwargs):
        pass

    def doc_description(self, help_command, **kwargs):
        doc = help_command.doc
        service_model = help_command.obj
        doc.style.h2('Description')
        # TODO: need a documentation attribute.
        doc.include_doc_string(service_model.documentation)

    def doc_subitems_start(self, help_command, **kwargs):
        doc = help_command.doc
        doc.style.h2('Available Commands')
        doc.style.toctree()

    def doc_subitem(self, command_name, help_command, **kwargs):
        doc = help_command.doc
        subcommand = help_command.command_table[command_name]
        subcommand_table = getattr(subcommand, 'subcommand_table', {})
        # If the subcommand table has commands in it,
        # direct the subitem to the command's index because
        # it has more subcommands to be documented.
        if (len(subcommand_table) > 0):
            file_name = '%s/index' % command_name
            doc.style.tocitem(command_name, file_name=file_name)
        else:
            doc.style.tocitem(command_name)


class OperationDocumentEventHandler(CLIDocumentEventHandler):

    AWS_DOC_BASE = 'https://docs.aws.amazon.com/goto/WebAPI'

    def doc_description(self, help_command, **kwargs):
        doc = help_command.doc
        operation_model = help_command.obj
        doc.style.h2('Description')
        doc.include_doc_string(operation_model.documentation)
        self._add_webapi_crosslink(help_command)
        self._add_top_level_args_reference(help_command)

    def _add_top_level_args_reference(self, help_command):
        help_command.doc.writeln('')
        help_command.doc.write("See ")
        help_command.doc.style.internal_link(
            title="'aws help'",
            page='/reference/index'
        )
        help_command.doc.writeln(' for descriptions of global parameters.')

    def _add_webapi_crosslink(self, help_command):
        doc = help_command.doc
        operation_model = help_command.obj
        service_model = operation_model.service_model
        service_uid = service_model.metadata.get('uid')
        if service_uid is None:
            # If there's no service_uid in the model, we can't
            # be certain if the generated cross link will work
            # so we don't generate any crosslink info.
            return
        doc.style.new_paragraph()
        doc.write("See also: ")
        link = '%s/%s/%s' % (self.AWS_DOC_BASE, service_uid,
                             operation_model.name)
        doc.style.external_link(title="AWS API Documentation", link=link)
        doc.writeln('')

    def _json_example_value_name(self, argument_model, include_enum_values=True):
        # If include_enum_values is True, then the valid enum values
        # are included as the sample JSON value.
        """
        if isinstance(argument_model, StringShape):
            if argument_model.enum and include_enum_values:
                choices = argument_model.enum
                return '|'.join(['"%s"' % c for c in choices])
            else:
                return '"string"'
        """
        if argument_model.type_name == 'boolean':
            return 'true|false'
        else:
            return '%s' % argument_model.type_name

    def _json_example(self, doc, argument_model, stack):
        if argument_model.name in stack:
            # Document the recursion once, otherwise just
            # note the fact that it's recursive and return.
            if stack.count(argument_model.name) > 1:
                if argument_model.type_name == 'structure':
                    doc.write('{ ... recursive ... }')
                return
        stack.append(argument_model.name)
        try:
            self._do_json_example(doc, argument_model, stack)
        finally:
            stack.pop()

    def _do_json_example(self, doc, argument_model, stack):
        if argument_model.type_name == 'list':
            doc.write('[')
            if argument_model.member.type_name in SCALAR_TYPES:
                doc.write('%s, ...' % self._json_example_value_name(argument_model.member))
            else:
                doc.style.indent()
                doc.style.new_line()
                self._json_example(doc, argument_model.member, stack)
                doc.style.new_line()
                doc.write('...')
                doc.style.dedent()
                doc.style.new_line()
            doc.write(']')
        elif argument_model.type_name == 'map':
            doc.write('{')
            doc.style.indent()
            key_string = self._json_example_value_name(argument_model.key)
            doc.write('%s: ' % key_string)
            if argument_model.value.type_name in SCALAR_TYPES:
                doc.write(self._json_example_value_name(argument_model.value))
            else:
                doc.style.indent()
                self._json_example(doc, argument_model.value, stack)
                doc.style.dedent()
            doc.style.new_line()
            doc.write('...')
            doc.style.dedent()
            doc.write('}')
        elif argument_model.type_name == 'structure':
            self._doc_input_structure_members(doc, argument_model, stack)

    def _doc_input_structure_members(self, doc, argument_model, stack):
        doc.write('{')
        doc.style.indent()
        doc.style.new_line()
        members = argument_model.members
        for i, member_name in enumerate(members):
            member_model = members[member_name]
            member_type_name = member_model.type_name
            if member_type_name in SCALAR_TYPES:
                doc.write('"%s": %s' % (member_name,
                    self._json_example_value_name(member_model)))
            elif member_type_name == 'structure':
                doc.write('"%s": ' % member_name)
                self._json_example(doc, member_model, stack)
            elif member_type_name == 'map':
                doc.write('"%s": ' % member_name)
                self._json_example(doc, member_model, stack)
            elif member_type_name == 'list':
                doc.write('"%s": ' % member_name)
                self._json_example(doc, member_model, stack)
            if i < len(members) - 1:
                doc.write(',')
                doc.style.new_line()
        doc.style.dedent()
        doc.style.new_line()
        doc.write('}')

    def doc_option_example(self, arg_name, help_command, event_name, **kwargs):
        doc = help_command.doc
        cli_argument = help_command.arg_table[arg_name]
        if cli_argument.group_name in self._arg_groups:
            if cli_argument.group_name in self._documented_arg_groups:
                # Args with group_names (boolean args) don't
                # need to generate example syntax.
                return
        argument_model = cli_argument.argument_model
        """
        service_id, operation_name = \
            find_service_and_method_in_event_name(event_name)
        docgen = ParamShorthandDocGen()
        if docgen.supports_shorthand(cli_argument.argument_model):
            example_shorthand_syntax = docgen.generate_shorthand_example(
                cli_argument, service_id, operation_name)
            if example_shorthand_syntax is None:
                # If the shorthand syntax returns a value of None,
                # this indicates to us that there is no example
                # needed for this param so we can immediately
                # return.
                return
            if example_shorthand_syntax:
                doc.style.new_paragraph()
                doc.write('Shorthand Syntax')
                doc.style.start_codeblock()
                for example_line in example_shorthand_syntax.splitlines():
                    doc.writeln(example_line)
                doc.style.end_codeblock()
        """
        if argument_model is not None and argument_model.type_name == 'list' and \
                argument_model.member.type_name in SCALAR_TYPES:
            # A list of scalars is special.  While you *can* use
            # JSON ( ["foo", "bar", "baz"] ), you can also just
            # use the argparse behavior of space separated lists.
            # "foo" "bar" "baz".  In fact we don't even want to
            # document the JSON syntax in this case.
            member = argument_model.member
            doc.style.new_paragraph()
            doc.write('Syntax')
            doc.style.start_codeblock()
            example_type = self._json_example_value_name(
                member, include_enum_values=False)
            doc.write('%s %s ...' % (example_type, example_type))
            # if isinstance(member, StringShape) and member.enum:
                # If we have enum values, we can tell the user
                # exactly what valid values they can provide.
                # self._write_valid_enums(doc, member.enum)
            doc.style.end_codeblock()
            doc.style.new_paragraph()
        elif cli_argument.cli_type_name not in SCALAR_TYPES:
            doc.style.new_paragraph()
            doc.write('JSON Syntax')
            doc.style.start_codeblock()
            self._json_example(doc, argument_model, stack=[])
            doc.style.end_codeblock()
            doc.style.new_paragraph()

    def _write_valid_enums(self, doc, enum_values):
        doc.style.new_paragraph()
        doc.write("Where valid values are:\n")
        for value in enum_values:
            doc.write("    %s\n" % value)
        doc.write("\n")

    def doc_output(self, help_command, event_name, **kwargs):
        doc = help_command.doc
        doc.style.h2('Output')
        operation_model = help_command.obj
        output_shape = operation_model.output_shape
        if output_shape is None or not output_shape.members:
            doc.write('None')
        else:
            for member_name, member_shape in output_shape.members.items():
                self._doc_member(doc, member_name, member_shape, stack=[])

    def doc_options_end(self, help_command, **kwargs):
        self._add_top_level_args_reference(help_command)
