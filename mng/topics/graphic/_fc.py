import re
import uuid
import json
import pprint


class FusionChart(object):
    """Create an object that represents a graphic in the web application,
    with methods for validating and formatting the parameters and delivering
    a structure in dict to post the API
    """

    def __init__(
            self,
            name: str,
            title: str,
            caption: str,
            subcaption: str,
            prefix: str,
            format: str,
            type_graph: str,
            description_value: str,
            cid=None) -> None:

        self.cid = cid
        self.uid = self.__create_uid(name)
        self.caption = caption
        self.subcaption = subcaption
        self.yAxis_plot_value = description_value
        self.yAxis_plot_type = type_graph   # line
        self.yAxis_format_prefix = prefix
        self.yAxis_title = title

        self.schema = self.__create_schema(title, format)

    def __create_stftime(self, stftime: str) -> str:
        strf = '-'.join('%'+i for i in stftime.split('-'))
        if ' ' in strf:
            day, hour = strf.split(' ')
            nhour = ':'.join('%'+i for i in hour.split(':'))
            strf = ' '.join([day, nhour])

        # re_data = re.compile(r'^%m')
        if re.compile(r'^%m').match(strf):
            strf = '%Y-'+strf
        # strftime to pattern "^Y-m-d"

        return strf

    def __create_schema(self, title: str, stftime: str) -> list:
        if '%' not in stftime:
            stftime = self.__create_stftime(stftime)

        return json.dumps([
            {
                'name': 'Time',
                'type': 'date',
                'format': stftime
            },
            {
                'name': 'title',
                'type': 'number'
            }
        ])

    def __create_uid(self, name: str) -> str:
        step_uid = str(uuid.uuid4()).split('-')[1]
        step_name = name[:14].replace(' ', '_')

        return '%s_%s' % (step_uid, step_name)

    @property
    def pprint(self) -> None:
        pp = pprint.PrettyPrinter(indent=2, compact=True, width=50)
        pp.pprint(self.__dict__)

    @property
    def __dict__(self):
        return {
            'uid': self.uid,
            'cid': self.cid,
            'caption': self.caption,
            'subcaption': self.subcaption,
            'yAxis_plot_value': self.yAxis_plot_value,
            'yAxis_plot_type': self.yAxis_plot_type,
            'yAxis_format_prefix': self.yAxis_format_prefix,
            'yAxis_title': self.yAxis_title,
            'schema': self.schema
        }
