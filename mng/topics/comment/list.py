from ...commands import BasicCommand
from ...http import request
from ...utils import lookup_config, write_stdout, write_stdout_pprint


class CommentListCommand(BasicCommand):

    NAME = 'list'

    DESCRIPTION = (
        'Lista todos os comentários de todas as anotações.')

    SYNOPSIS = ' $ mng comment list'

    EXAMPLES = (
        '   $ mng comment list\n'
    )


    def _run_main(self, args, parsed_globals) -> None:
        comments = self.__list_comments(args)

        if comments is None:
            write_stdout('\n>> Ops... error, see log for more details.')
            return

        print()
        write_stdout_pprint(comments, width=60, indent=4)

    def __list_comments(self, args) -> list or None:
        url = 'http://%s:%s/api/comment/' % (lookup_config('address_api'), lookup_config('port_api'))

        sucessful, data = request(
            url,
            method='GET',
            headers={'Authorization': 'Basic %s' % lookup_config('base64auth')}
        )

        return data if sucessful else None
