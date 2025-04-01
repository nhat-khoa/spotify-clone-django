import uuid
import os
from datetime import datetime


def generate_unique_filename(instance, filename):
    # Lấy tên class của model
    model_name = instance.__class__.__name__.lower()
    
    # # Lấy ngày hiện tại để tạo thư mục theo năm/tháng
    # now = datetime.now()
    # date_path = f"{now.year}/{now.month:02d}"
    
    # Lấy phần mở rộng của file
    ext = filename.split('.')[-1]
    
    # Tạo tên file mới với UUID
    unique_filename = f"{str(uuid.uuid4())}.{ext}"
    
    # Trả về đường dẫn kết hợp
    return os.path.join(model_name + 's', unique_filename)