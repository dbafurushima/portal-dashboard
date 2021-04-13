from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.db import DatabaseError, DataError, IntegrityError, InternalError
from django.core.exceptions import ObjectDoesNotExist

from jsonschema import validate
from jsonschema import ValidationError

from .models import AppNote, Topic

from ..charts.zabbix.api import Zabbix, AccessDeniedCredentialException
from ..charts.fusioncharts import FusionTable, TimeSeries, FusionCharts
from ..charts.models import Chart
from ..management.models import EnterpriseUser

from github import Github


@login_required
def view_list_graph(request):
    graphs = Chart.objects.filter(
        client=EnterpriseUser.objects.get(
            user=request.user
        ).enterprise
    )

    return render(
        request,
        'pages/portal/list-graph.html',
        {
            'graphs': graphs
        }
    )


@login_required
def home_view(request):
    """
    if not request.user.is_superuser:
        return render(request, 'pages/portal/home.html')

    zabbix_graph = 'void'
    try:
        zb = Zabbix(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        raw_data = zb.get_history_from_itemids('31359')

        zabbix_data = [[datetime.fromtimestamp(data[0]).strftime('%Y-%m-%d %H:%M'), data[1]] for data in raw_data]

        schema = '[{"name": "Time","type": "date","format": "%Y-%m-%d %H:%M"}, {"name": "Usage CPU","type": "number"}]'

        fusion_table = FusionTable(schema, zabbix_data)
        time_series = TimeSeries(fusion_table)

        if request.session.get('theme', 'dark') == 'dark':
            time_series.AddAttribute("chart", "{showLegend: 0, theme: 'candy'}")

        time_series.AddAttribute("caption", "{text: '%s'}" % 'unknown 01')
        time_series.AddAttribute("subcaption", "{text: '%s'}" % 'unknown 02')
        time_series.AddAttribute("yAxis", (
                "[{"
                "plot: {"
                "value: '%s',"
                "type: '%s'"
                "},"
                "format: {"
                "prefix: '%s'"
                "},"
                "title: '%s'"
                "}]" % ('usage cpu is', 'line',
                        '%/min', 'usage_cpu_vm0'))
        )

        fusion_chart = FusionCharts(
            "timeseries",
            "zabbix",
            "100%",
            450,
            "chart-zabbix", "json",
            time_series
        )

        zabbix_graph = fusion_chart.render()
    except AccessDeniedCredentialException:
        pass
    except Exception as err:
        pass

    g = Github(settings.GITHUB_TOKEN)
    repo = g.get_repo("dbafurushima/portal-dashboard")

    contents = repo.get_top_paths()
    graph_01_len_paths = len(contents)
    graph_01_counts = [content.count for content in contents]

    contents = repo.get_clones_traffic()
    graph_02_traffic = contents.get('count')
    graph_02_counts = [content.count for content in contents.get('clones')]
    graph_02_labels = [x for x in range(1, len(graph_01_counts) + 1)]

    contents = repo.get_views_traffic()
    graph_03_traffic = contents.get('count')
    graph_03_counts = [content.count for content in contents.get('views')]

    open_issues = repo.get_issues(state='open')
    issues = [
        {
            'id': issue.number,
            'title': issue.title
        } for issue in open_issues]

    return render(
        request,
        'pages/management/index.html',
        {
            'data': {
                'graph_01': {
                    'len': graph_01_len_paths,
                    'counts': graph_01_counts
                },
                'graph_02': {
                    'len': graph_02_traffic,
                    'counts': graph_02_counts,
                    'labels': graph_02_labels
                },
                'graph_03': {
                    'len': graph_03_traffic,
                    'counts': graph_03_counts
                }
            },
            'issues': issues,
            'zabbix': zabbix_graph
        }
    )
    """
    notes_by_topics = [
        {
            topic: AppNote.objects.filter(topic=topic).filter(display=True)
        } for topic in Topic.objects.filter(owner=request.user)
    ]

    return render(
        request,
        'pages/portal/home.html',
        {
            'topics': Topic.objects.filter(owner=request.user),
            'notes': AppNote.objects.filter(owner=request.user).filter(display=True),
            'notes_by_topics': notes_by_topics
        })


SCHEMA_CREATE_TOPIC = {
    "type": "object",
    "properties": {"title": {"type": "string"}, "color": {"type": "string"}, }}


@login_required
def route_create_topic(request):
    if request.method != 'POST':
        return JsonResponse({})

    raw_data = dict(request.POST)
    try:
        raw_data = {key: value[0] for (key, value) in raw_data.items()}
    except IndexError:
        pass
    try:
        validate(SCHEMA_CREATE_TOPIC, raw_data)
    except ValidationError as err:
        return JsonResponse(
            {'code': 400, 'msg': '%s' % err})

    topic = Topic(
        name=raw_data.get('name').lower(),
        color=raw_data.get('color'),
        owner=request.user
    )

    try:
        topic.save()
    except DatabaseError as err:
        return JsonResponse(
            {'code': 500, 'msg': '%s' % err})

    return JsonResponse(
        {'code': 200, 'msg': '%s' % topic})


SCHEMA_CREATE_NOTE = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "text": {"type": "string"},
        "topic": {"type": "string"}
    }
}


@login_required
def route_create_note(request):

    if request.method != 'POST':
        return JsonResponse({})

    raw_data = dict(request.POST)
    try:
        raw_data = {key: value[0] for (key, value) in raw_data.items()}
    except IndexError:
        pass

    try:
        validate(SCHEMA_CREATE_NOTE, raw_data)
    except ValidationError as err:
        return JsonResponse({'code': 400, 'msg': '%s' % err})

    try:
        topic = Topic.objects.get(name=raw_data.get('topic'))
    except Topic.DoesNotExist as err:
        return JsonResponse({'code': 500, 'msg': '%s' % err})

    note = AppNote(
        title=raw_data.get('title'),
        text=raw_data.get('text'),
        topic=topic,
        owner=request.user,
        display=True
    )

    try:
        note.save()
    except DatabaseError as err:
        return JsonResponse(
            {'code': 500, 'msg': '%s' % err})

    return JsonResponse(
        {'code': 200, 'msg': '%s' % note})


SCHEMA_FAVORITE_NOTE = {
    "type": "object",
    "properties": {"title": {"type": "string"}, "act": {"type": "string"}}}


@login_required
def route_fav_note(request):
    if request.method != 'POST':
        return JsonResponse({})

    raw_data = dict(request.POST)
    try:
        raw_data = {key: value[0] for (key, value) in raw_data.items()}
    except IndexError:
        pass

    try:
        validate(SCHEMA_FAVORITE_NOTE, raw_data)
    except ValidationError as err:
        return JsonResponse({'code': 400, 'msg': '%s' % err})

    try:
        note = AppNote.objects.get(title=raw_data.get('name'))
    except AppNote.DoesNotExist as err:
        return JsonResponse({'code': 500, 'msg': '%s' % err})
    else:
        note.favorite = True if raw_data.get('act') == "true" else False
        try:
            note.save()
        except (DatabaseError, DataError, InternalError, IntegrityError) as err:
            return JsonResponse({'code': 500, 'msg': '%s' % err})
        else:
            return JsonResponse({'code': 200, 'msg': note.favorite})


SCHEMA_DELETE_NOTE = {
    "type": "object",
    "properties": {"title": {"type": "string"}}}


@login_required
def route_delete_note(request):
    if request.method != 'POST':
        return JsonResponse({})

    raw_data = dict(request.POST)
    try:
        raw_data = {key: value[0] for (key, value) in raw_data.items()}
    except IndexError:
        pass

    try:
        validate(SCHEMA_FAVORITE_NOTE, raw_data)
    except ValidationError as err:
        return JsonResponse({'code': 400, 'msg': '%s' % err})

    try:
        note = AppNote.objects.get(title=raw_data.get('title'))
    except AppNote.DoesNotExist as err:
        return JsonResponse({'code': 500, 'msg': '%s' % err})
    else:
        note.display = False
        try:
            note.save()
        except (DatabaseError, DataError, InternalError, IntegrityError) as err:
            return JsonResponse({'code': 500, 'msg': '%s' % err})
        else:
            return JsonResponse({'code': 200, 'msg': note.favorite})


SCHEMA_EDIT_NOTE = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "text": {"type": "string"},
        "topic": {"type": "string"},
        "id": {"type": "integer"}
    }
}


@login_required
def route_edit_note(request):

    if request.method != 'POST':
        return JsonResponse({})

    raw_data = dict(request.POST)
    try:
        raw_data = {key: value[0] for (key, value) in raw_data.items()}
    except IndexError:
        pass

    try:
        validate(SCHEMA_CREATE_NOTE, raw_data)
    except ValidationError as err:
        return JsonResponse({'code': 400, 'msg': '%s' % err})

    try:
        topic = Topic.objects.get(name=raw_data['topic'])
    except (Topic.DoesNotExist, ObjectDoesNotExist, DatabaseError) as err:
        return JsonResponse({'code': 500, 'msg': '%s' % err})

    try:
        note = AppNote.objects.get(id=int(raw_data.get('id')))
    except AppNote.DoesNotExist as err:
        return JsonResponse({'code': 500, 'msg': '%s' % err})

    note.title = raw_data['title']
    note.topic = topic
    note.text = raw_data['text']

    try:
        note.save()
    except DatabaseError as err:
        return JsonResponse(
            {'code': 500, 'msg': '%s' % err})

    return JsonResponse(
        {'code': 200, 'msg': '%s' % note})
