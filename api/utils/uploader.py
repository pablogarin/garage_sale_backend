import os
from werkzeug.utils import secure_filename


def upload_files(request):
    UPLOAD_FOLDER = "/app/uploads"
    files = request.files
    urls = []
    if len(files) == 0:
        raise Exception('No file part')
    for filename in files:
        file = files[filename]
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        urls.append(f"/img/{filename}")
    return urls