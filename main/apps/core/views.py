from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.apps import apps

def db_metadata_view(request):
    metadata = []

    with connection.cursor() as cursor:
        table_names = connection.introspection.table_names()

        for table_name in table_names:
            try:
                # Lấy thông tin các cột của bảng
                columns = [col.name for col in connection.introspection.get_table_description(cursor, table_name)]
            except Exception as e:
                # Một số bảng có thể bị lỗi introspection (hiếm), nên catch cho chắc
                continue

            metadata.append({
                "table": table_name,
                "columns": columns
            })

    # Sắp xếp theo tên bảng
    metadata.sort(key=lambda item: item["table"])

    return JsonResponse(metadata, safe=False)

@require_GET
def multi_table_data_view(request):
    fixed_tables = {
        "albums_album": ["id", "title", "artist_id","is_premium"],
        "artists_artist": ["id", "name"],
        "tracks_track": ["id", "title", "duration_ms", "popularity", "album_id","artist_id", "is_premium"]
    }

    data = {}

    for table, fields in fixed_tables.items():
        try:
            model = next(
                m for m in apps.get_models()
                if m._meta.db_table == table
            )
            rows = list(model.objects.all().values(*fields)[:50])
            data[table] = rows
        except StopIteration:
            data[table] = f"Bảng '{table}' không tồn tại"

    return JsonResponse(data, safe=False)