# Zadanie 2 – Implementacja Full Stack (Django stack) w klastrze Minikube

W ramach zadania zaimplementowano przykładową aplikację full-stack w oparciu o  
**Django stack (JavaScript – Python – Django – MySQL)**, zgodny z listą *Popular Stacks*
przedstawioną na stronie W3Schools.

Aplikacja została uruchomiona w klastrze **Minikube** i jest dostępna z zewnątrz klastra
pod adresem:

- http://brilliantapp.zad

---

## 1) Opis aplikacji i wybranego stack-a

**BrilliantApp** to przykładowa aplikacja webowa typu „notes”, składająca się z warstwy
frontend, backend oraz bazy danych.

### Frontend
- Prosta strona HTML z osadzonym kodem **JavaScript**
- Komunikacja z backendem realizowana za pomocą zapytań HTTP (`fetch`)

### Backend
- Aplikacja serwerowa **Django (Python)**
- Udostępniane endpointy:
  - `/` – strona główna aplikacji
  - `/api/health` – endpoint zdrowia aplikacji
  - `/api/notes` – endpoint zwracający dane z bazy MySQL w formacie JSON

### Baza danych
- **MySQL**
- Przechowuje dane aplikacji (np. notatki)

### Istotne cechy wdrożenia w Minikube
- Backend Django uruchomiony jako **Deployment** (skalowalność)
- MySQL uruchomiony jako **StatefulSet** z **PersistentVolumeClaim**
  w celu zapewnienia trwałości danych
- Konfiguracja aplikacji przechowywana w **ConfigMap**
- Dane wrażliwe (hasła) przechowywane w **Secret**
- Dostęp zewnętrzny do aplikacji zrealizowany przez **Ingress NGINX**

---

## 2) Architektura wdrożenia w klastrze Minikube

Architektura logiczna rozwiązania:

- Ingress NGINX  
- Service `brilliantapp-svc` (ClusterIP)  
- Deployment `brilliantapp` (Django, 2 repliki)  
- Service `mysql` (ClusterIP)  
- StatefulSet `mysql` (1 replika + PVC)

---

## 3) Pliki konfiguracyjne wdrożenia

### Manifesty Kubernetes (katalog `k8s/`)
- `00-namespace.yaml` – Namespace `brilliant`
- `10-secret-mysql.yaml` – Secret z hasłami do MySQL
- `20-configmap-django.yaml` – ConfigMap z konfiguracją aplikacji Django
- `30-pvc-mysql.yaml` – PersistentVolumeClaim dla MySQL
- `40-statefulset-mysql.yaml` – StatefulSet `mysql`
- `50-service-mysql.yaml` – Service `mysql` typu ClusterIP
- `60-deployment-django.yaml` – Deployment `brilliantapp`
- `70-service-django.yaml` – Service `brilliantapp-svc` typu ClusterIP
- `80-ingress.yaml` – Ingress udostępniający aplikację pod adresem `brilliantapp.zad`

### Kod aplikacji
- `app/` – źródła aplikacji Django
- `app/Dockerfile` – definicja obrazu kontenera backendu
- `app/requirements.txt` – zależności Pythona

---

## 4) Uruchomienie klastra Minikube

- `minikube delete`
- `minikube start --driver=docker`

Weryfikacja:
- `minikube status`
- `kubectl get nodes`

---

## 5) Aktywacja Ingress NGINX

- `minikube addons enable ingress`

Weryfikacja:
- `minikube addons list | grep ingress`
- `kubectl get all -n ingress-nginx`

---

## 5a) Aktywacja rejestru obrazów Minikube (registry)

W celu umożliwienia pracy z obrazami kontenerów w środowisku wielowęzłowego klastra
Minikube aktywowano wbudowany rejestr obrazów.

- `minikube addons enable registry`

Weryfikacja:
- `kubectl get pods -n kube-system | grep registry`
- `kubectl get svc -n kube-system | grep registry`

---

## 6) Budowa obrazu aplikacji

Budowa obrazu kontenera backendu Django:

- `docker build -t brilliantapp:1.0 ./app`

Weryfikacja:
- `docker images | grep brilliantapp`

---

## 7) Wdrożenie zasobów Kubernetes

- `kubectl apply -f k8s/00-namespace.yaml`
- `kubectl apply -f k8s/10-secret-mysql.yaml`
- `kubectl apply -f k8s/20-configmap-django.yaml`
- `kubectl apply -f k8s/30-pvc-mysql.yaml`
- `kubectl apply -f k8s/40-statefulset-mysql.yaml`
- `kubectl apply -f k8s/50-service-mysql.yaml`
- `kubectl apply -f k8s/60-deployment-django.yaml`
- `kubectl apply -f k8s/70-service-django.yaml`
- `kubectl apply -f k8s/80-ingress.yaml`

Weryfikacja:
- `kubectl get all -n brilliant`
- `kubectl get pvc -n brilliant`
- `kubectl get ingress -n brilliant`
- `kubectl describe ingress brilliantapp-ingress -n brilliant`

---

## 8) Udostępnienie aplikacji na zewnątrz klastra

Uruchomienie tunelu Ingress:

- `sudo -E HOME=$HOME minikube tunnel -p minikube`

Dodanie wpisu DNS (symulacja):
- wpis `127.0.0.1 brilliantapp.zad` w pliku `/etc/hosts`

---

## 9) Testy poprawności działania aplikacji

- Test strony głównej:
  - `curl http://brilliantapp.zad/`
- Test endpointu zdrowia:
  - `curl http://brilliantapp.zad/api/health`
- Test komunikacji z bazą danych:
  - `curl http://brilliantapp.zad/api/notes`
- Test zapisu danych:
  - `curl -X POST http://brilliantapp.zad/api/notes -H "Content-Type: application/json" -d '{"text":"pierwsza notatka"}'`

Poprawne odpowiedzi potwierdzają:
- poprawne działanie Ingress
- komunikację frontend ↔ backend
- komunikację backend ↔ MySQL
- trwałość danych w bazie

---

## Wyniki

- Aplikacja została poprawnie wdrożona w klastrze Minikube
- Zastosowano pełny Django stack (JavaScript – Django – MySQL)
- Dostęp zewnętrzny do aplikacji zrealizowano przez Ingress NGINX
- Testy potwierdziły poprawność działania wszystkich warstw aplikacji

---

## Zrzuty ekranu

Zrzuty ekranu potwierdzające poprawność działania rozwiązania znajdują się w folderze:

**zadanie 2 – zrzuty ekranu**
