# **Instalacja shared**

### **Opis katalogów**

- **`shared/`**: Zawiera pliki `.proto`, które są wykorzystywane do generowania kodu Python (`*_pb2.py`
  i `*_pb2_grpc.py`) za pomocą `grpc_tools.protoc`.
- **`scripts/`**: Zawiera skrypty pomocnicze, takie jak `generate_proto_files.sh`, który automatyzuje proces generowania
  kodu z plików `.proto`.

---

### **Instalacja**

1. Do folderu `shared/` wrzucamy pliki `.proto`.
2. Skrypt `generate_proto_files.sh` generuje pliki `*_pb2.py` oraz `*_pb2_grpc.py`.

---

### **Modyfikacja Dockerfile**

Aby obsłużyć generowanie plików w kontenerze Dockera, należy dodać poniższe linie do pliku `Dockerfile`:

```dockerfile
COPY ./shared /code/shared

COPY ./scripts/generate_proto_files.sh /code/generate_proto_files.sh

RUN chmod +x /code/generate_proto_files.sh
ENTRYPOINT ["/bin/sh", "/code/generate_proto_files.sh"]
```

### **Uruchomienie lokalnie**

Utworz w serwise folder `shared` i wrzuc do niego pliki .proto. Wygeneruj pliki `*_pb2.py` oraz `*_pb2_grpc.py` za pomocą skryptu `generate_proto_files.sh`.

Do `.gitignore` dodaj folder `shared`

Do `.dockerignore` dodaj folder `shared`

# Instalacja MQTT:

Tworzymy plik passwd w którym umieszczamy login i hasło do brokera MQTT w formacie:

```
login:hasło
```

Następnie uruchamiamy skrypt:

```
docker exec mosquitto mosquitto_passwd -U /etc/mosquitto/passwd
```

jesli chcemy dodac nowych uzytkownikow:

```
docker exec mosquitto mosquitto_passwd -b /etc/mosquitto/passwd user password
```

Nalezy pamietac aby zrestartowac kontener mosquitto po dodaniu nowych uzytkownikow.


