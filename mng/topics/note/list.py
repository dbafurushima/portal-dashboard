from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config, write_stdout, write_stdout_pprint


class NoteListCommand(BasicCommand):

    NAME = 'list'

    DESCRIPTION = (
        'Lista todas anotações que não estão marcadas como excluidas.')

    SYNOPSIS = ' $ mng note list'

    EXAMPLES = (
        'Listando anotações criadas\n'
        '\n'
        ' $ mng notes list\n'
        '\n'
        "[   {   'comments': [],\n"
        "   'id': 9,\n"
        "   'msg': \"atualizar documentação do comando 'dev'\",\n"
        "   'subject': 'dev',\n"
        "   'timestamp': '2020-11-06 22:06:28'}]\n"
    )


    def _run_main(self, args, parsed_globals) -> None:
        notes = self.__list_notes(args)

        if notes is None:
            write_stdout('\n>> Ops... error, see log for more details.')
            return

        print()
        write_stdout_pprint(notes, width=60, indent=4)

    def __list_notes(self, args) -> list or None:
        url = 'http://%s:%s/api/note/' % (lookup_config('address_api'), lookup_config('port_api'))

        sucessful, data = request(
            url,
            method='GET',
            headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
        )

        return data if sucessful else None
