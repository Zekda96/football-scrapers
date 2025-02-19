import os
from supabase import create_client
from json import loads
from pandas import DataFrame

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def write_to_supabase(table_name: str, df: DataFrame, method: str):
    """
    """

    data = loads(df.to_json(orient="records"))
    try:
        if method == "upsert":
            response = supabase.table(table_name)\
            .upsert(data)\
            .execute()
        elif method == "insert":
            response = supabase.table(table_name)\
            .insert(data)\
            .execute()
        return response
    except Exception as exception:
        return exception
