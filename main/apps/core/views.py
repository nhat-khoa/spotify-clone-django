from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt

import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

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

def get_db_metadata():
    metadata_lines = []

    with connection.cursor() as cursor:
        table_names = connection.introspection.table_names()

        for table_name in table_names:
            try:
                columns = [col.name for col in connection.introspection.get_table_description(cursor, table_name)]
                column_list = ", ".join(columns)
                metadata_lines.append(f"{table_name} ({column_list})")
            except Exception:
                continue

    metadata_lines.sort()
    return "\n".join(metadata_lines)

def get_selected_metadata():
    metadata_lines = []
    selected_tables = ["albums_album", "artists_artist", "tracks_track"]

    with connection.cursor() as cursor:
        for table_name in selected_tables:
            try:
                columns = [col.name for col in connection.introspection.get_table_description(cursor, table_name)]
                column_list = ", ".join(columns)
                metadata_lines.append(f"{table_name} ({column_list})")
            except Exception:
                continue

    return "\n".join(metadata_lines)

@csrf_exempt
@require_POST
def chat_with_data(request):
    try:
        body = json.loads(request.body)
        user_prompt = body.get("prompt")
        if not user_prompt:
            return JsonResponse({"error": "Missing 'prompt' in request body"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    metadata = get_db_metadata()

    # Hỏi LLM xem câu hỏi có cần query DB không
    check_prompt = f"""
        Câu hỏi sau đây có cần truy vấn dữ liệu từ cơ sở dữ liệu không?
        Câu hỏi: "{user_prompt}"
        Trả lời ngắn gọn: "yes" hoặc "no".
        Không giải thich thêm gì cả.
        Nhấn mạnh lại là chỉ trả lời "yes" hoặc "no".
    """

    check_res = requests.post(OLLAMA_URL, json={
        "model": "llama3:8b",
        "prompt": check_prompt,
        "stream": False
    })

    check_response = check_res.json()["response"].strip().lower()
    print(f"need data: {check_response}")

    # Nếu không cần query DB, chỉ cần trả lời thẳng
    if "no" in check_response:
        direct_answer_prompt = f"""
            Trả lời câu hỏi sau bằng tiếng Việt ngắn gọn, thân thiện, dễ hiểu:
            "{user_prompt}"
        """
        answer_res = requests.post(OLLAMA_URL, json={
            "model": "llama3:8b",
            "prompt": direct_answer_prompt,
            "stream": False
        })
        return JsonResponse({
            "answer": answer_res.json()["response"].strip(),
            "sql": None,
            "data_preview": None
        })

    # Nếu cần query DB thực hiện tiếp tục
    gen_sql_prompt = f"""
        Dưới đây là metadata của database:\n{metadata}\n
        Hãy viết một câu SQL (PostgreSQL) để trả lời câu hỏi sau:\n"{user_prompt}"
        Hãy trả về **chỉ duy nhất một câu SQL** để trả lời câu hỏi trên.
        **Nếu trong bảng cần select có cột chứa giá trị là uuid của bảng khác thì hãy join các bảng lại với nhau để lấy dữ liệu.**
        **Bắt buộc phải luôn luôn select * để lấy tất cả các cột trong bảng.**
        **Không được viết thêm bất kỳ giải thích hoặc chú thích nào.**
        Không được sử dụng markdown, không được bao quanh bởi ```sql.
    """

    res1 = requests.post(OLLAMA_URL, json={
        "model": "llama3:8b",
        "prompt": gen_sql_prompt,
        "stream": False
    })

    sql_query = res1.json()["response"].strip()
    print(f"SQL query: {sql_query}")

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
    except Exception as e:
        return JsonResponse({"error": f"SQL execution failed: {e}", "sql": sql_query}, status=500)

    data_preview = [dict(zip(columns, row)) for row in rows[:5]]
    gen_answer_prompt = f"""
        Dữ liệu sau được trả về từ database để trả lời câu hỏi: "{user_prompt}"
        Dữ liệu: {data_preview}

        Hãy viết một câu trả lời ngắn gọn bằng tiếng Việt, **bắt buộc phải là tiếng việt**,
        dễ hiểu cho người dùng, được trình bày dưới dạng HTML đẹp mắt với các yêu cầu sau:

        - Sử dụng các thẻ HTML cơ bản như: <p>, <ul>, <li>, <strong>, <br>.
        - Dùng <strong> để in đậm các thông tin quan trọng như tên bài hát, nghệ sĩ, ngày phát hành...
        - Dùng <br> hoặc <ul>/<li> để xuống dòng hoặc hiển thị danh sách.
        - Không viết thêm bất kỳ giải thích nào ngoài nội dung trả lời.
        - Trả về duy nhất đoạn HTML (không markdown, không chú thích).
        - Bắt buộc thêm các icon emoji vào câu trả lời để tăng tính thân thiện.
        - Một số icon có thể sử dụng: 👋 🤔 😊 😅 🙏 🤖 🧑‍💻 🎯 🎉 🔄 📦 📌 ✅ ❌ ⚠️ 💡 📝 🔧 🔒 📂 🧠 🧪 📊 🔍 🔁 📥 📤 🚀 ⏳
        - Bắt buộc phải luôn luôn có emojis 😊 trong câu trả lời, tùy ngữ cảnh có thể thay đổi thành emojis khác

        Bắt đầu viết từ phần trả lời HTML ngay sau đây:
    """

    res2 = requests.post(OLLAMA_URL, json={
        "model": "llama3:8b",
        "prompt": gen_answer_prompt,
        "stream": False
    })

    return JsonResponse({
        "answer": res2.json()["response"].strip(),
        "sql": sql_query,
        "data_preview": data_preview
    })
