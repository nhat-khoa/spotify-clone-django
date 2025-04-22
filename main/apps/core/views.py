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
    table_names = request.GET.get("tables")
    if not table_names:
        return JsonResponse({"error": "Thiếu tham số tables"}, status=400)

    table_list = [name.strip() for name in table_names.split(",")]
    data = {}

    for table in table_list:
        try:
            # Lấy model tương ứng
            model = next(
                m for m in apps.get_models()
                if m._meta.db_table == table or m.__name__.lower() == table.lower()
            )
        except StopIteration:
            data[table] = f"Bảng '{table}' không tồn tại"
            continue

        # Lấy dữ liệu tối đa 50 row (giới hạn lại cho nhẹ)
        rows = list(model.objects.all()[:50].values())
        data[table] = rows

    return JsonResponse(data, safe=False)