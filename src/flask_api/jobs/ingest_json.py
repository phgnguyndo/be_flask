import os
import ijson
from flask_api.models.credential import Credential
from flask_api.app import db

DATA_DIR = "/home/phuong/Desktop/thuc_tap/json"
BATCH_SIZE = 500  # commit theo lô để tối ưu hiệu năng

def ingest_new_json_files():
    for filename in os.listdir(DATA_DIR):
        # if not filename.endswith(".json"):
        #     continue
        file_path = os.path.join(DATA_DIR, filename)

        # Kiểm tra nếu file đã được ghi vào DB (dựa theo tên file)
        if Credential.query.filter_by(filename=filename).first():
            continue

        credentials_to_add = []

        try:
            with open(file_path, "rb") as f:
                systems_data = ijson.items(f, "systems_data.item")
                for system_entry in systems_data:
                    system = system_entry.get("system")
                    for cred in system_entry.get("credentials", []):
                        password = cred.get("password")

                        if(len(password) > 255):
                            password = 'N/A'
                        credential = Credential(
                            filename=filename,
                            system=system,
                            software=cred.get("software"),
                            host=cred.get("host"),
                            username=cred.get("username"),
                            password=cred.get("password"),
                            domain=cred.get("domain"),
                            local_part=cred.get("local_part"),
                            email_domain=cred.get("email_domain"),
                            filepath=cred.get("filepath"),
                            stealer_name=cred.get("stealer_name"),
                        )
                        credentials_to_add.append(credential)

                        if len(credentials_to_add) >= BATCH_SIZE:
                            db.session.bulk_save_objects(credentials_to_add)
                            db.session.commit()
                            credentials_to_add.clear()

                # commit phần còn lại chưa đủ batch
                if credentials_to_add:
                    db.session.bulk_save_objects(credentials_to_add)
                    db.session.commit()

                print(f"Đã ghi toàn bộ dữ liệu từ {filename} vào DB")

        except Exception as e:
            db.session.rollback()
            print(f"Lỗi xử lý {filename}: {e}")
