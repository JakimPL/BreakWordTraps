from fastapi import FastAPI


app = FastAPI()

"""app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update this to the port your frontend is running on
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


def download_from_bucket(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Downloaded {source_blob_name} from bucket {bucket_name} to {destination_file_name}")

"""
"""@app.get("/run_pipeline/")
def read_root():
    bucket_name = "gs://breakthewordstraps-bucket-hackyeah/sample_video.mov"
    source_blob_name = "HY_2024_film_20.mp4"  # Ścieżka do pliku w buckecie
    local_file_name = "/tmp/HY_2024_film_20.mp4"  # Tymczasowe miejsce zapisania pliku
    
    # Pobierz plik z bucketa
    download_from_bucket(bucket_name, source_blob_name, local_file_name)
    
    # Uruchom pipeline z pobranym plikiem
    output = Pipeline(local_file_name)
    
    return {"message": "Pipeline uruchomiony", "output": output}
"""





@app.post("/items/")
def create_item(data: dict):
    return {"message": f"Item created successfully!"}
