from datetime import timedelta, datetime

from django.http import JsonResponse
from django.utils import timezone

from elasticsearch import Elasticsearch

INDEX_NAME = 'dogdrip'
TYPE_NAME = 'comments'


def get_comments_between_date(request):
    # get dates from queststring
    srt_date = request.GET.get('srt_date', None)
    end_date = request.GET.get('end_date', None)

    # convert date string to datetime object
    now = timezone.now()
    if srt_date == None:
        srt_date = now - timedelta(days=365)
    else:
        srt_date = datetime.strptime(srt_date, "%Y-%m-%d")

    if end_date == None:
        end_date = now
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # connect es and request query
    client = Elasticsearch()
    doc = {
        "_source": ["comments.content"],
        "query": {
            "nested": {
                "path": "comments",
                "query": {
                    "range": {
                        "comments.date": {
                            "time_zone": "+09:00",
                            "lte": end_date,
                            "gte": srt_date
                        }
                    }
                }
            }
        }
    }
    res = client.search(index=INDEX_NAME, doc_type=TYPE_NAME, body=doc)

    return JsonResponse(res)
