from datetime import datetime
import uuid

BATCH_ID = str(uuid.uuid4())

def add_metadata(record):
    record["_loaded_at"] = datetime.utcnow().isoformat()
    record["_source"] = "jolpica_api"
    record["_batch_id"] = BATCH_ID
    return record