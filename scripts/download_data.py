import os

import gdown

# Đường dẫn tuyệt đối đến thư mục 'data'
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
# Tạo thư mục 'data' nếu chưa tồn tại
os.makedirs(data_dir, exist_ok=True)

# Danh sách các tệp cần tải với định dạng (file_id, output_name)
files_to_download = [
    ('0B2X0QD6q79ZJbFI2ZlRBbTk1MjQ', 'non_skill_builder_data_new.csv'),
    ('0B2X0QD6q79ZJUFU1cjYtdGhVNjg', 'skill_builder_data.csv'),
    ('1NNXHFRxcArrU0ZJSb9BIL56vmUt5FhlE', 'skill_builder_data_corrected_collapsed.csv')
]

for file_id, output_name in files_to_download:
    # URL tải xuống
    url = f'https://drive.google.com/uc?id={file_id}'
    # Đường dẫn đầy đủ cho tệp đầu ra
    output = os.path.join(data_dir, output_name)
    # Tải tệp
    gdown.download(url, output, quiet=False)

#các con vợ chịu khó vào link tự tải về nhé file này tải nhiều quá gg ko cho tải tự do nữa