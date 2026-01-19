from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Note
import json

def index(request):
    html = """
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>BrilliantApp</title>
    </head>
    <body>
      <h1>BrilliantApp</h1>
      <p>To jest prosty frontend (HTML + JS). Kliknij, aby pobrać dane z backendu.</p>

      <button onclick="loadNotes()">Pobierz notatki</button>
      <button onclick="addNote()">Dodaj notatkę</button>

      <pre id="out" style="border:1px solid #ccc; padding:12px;"></pre>

      <script>
        async function loadNotes(){
          const r = await fetch('/api/notes');
          const j = await r.json();
          document.getElementById('out').textContent = JSON.stringify(j,null,2);
        }

        async function addNote(){
          const payload = {text: "notatka z JS " + new Date().toISOString()};
          const r = await fetch('/api/notes', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(payload)
          });
          const j = await r.json();
          document.getElementById('out').textContent = JSON.stringify(j,null,2);
        }
      </script>
    </body>
    </html>
    """
    return HttpResponse(html)

def health(request):
    return JsonResponse({"status": "ok"})

@csrf_exempt
def notes(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8") or "{}")
        text = data.get("text", "hello")
        n = Note.objects.create(text=text)
        return JsonResponse({"id": n.id, "text": n.text})

    items = list(Note.objects.values("id", "text"))
    return JsonResponse({"notes": items})
