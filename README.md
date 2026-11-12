# Entorno del examen

Antes de empezar, abre Docker Desktop y espera a que esté encendido.

- **Windows:** usa la terminal de Ubuntu en WSL2 y activa la integración de Docker con Ubuntu en Docker Desktop.
- **Mac:** usa la Terminal.

Ejecuta los siguientes comandos desde la carpeta de este proyecto:

```bash
bash scripts/preparar.sh
docker compose pull
docker compose up -d --wait airflow
bash scripts/examen.sh check
```

Cuando el último comando termine sin errores, abre http://localhost:8080 e inicia sesión con:

- Usuario: `estudiante`
- Contraseña: `examen-local`

Al terminar, detén los servicios con:

```bash
docker compose stop
```

No ejecutes `docker compose down -v`: borra los datos del entorno.
