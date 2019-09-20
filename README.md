# opentidal
Open Tidal - Memoria.

Proyecto elaborado durante el Hacklab / Artlab - Yaeltex en el marco de  MUTEK AR 2019.

Open Tidal.
Web based TidalCycles code repo and AI generator.

El propósito del Open Tidal es crear un repositorio en línea de código ejecutable en TidalCycles. Al mismo tiempo un algoritmo fundado sobre una red neuronal entrenada con el imput del sistema permite la navegación del repositorio y propone códigos automáticamente generados. Un plugin facilita el acceso del usuario al repositorio en forma directa desde Atom.

Equipo actual: Jimena Piano, Lais Macaria, Damián Silvani, Luis Tamagnini.

Trello board para seguir el desarrollo: https://trello.com/b/x2eIjf5o/opentidal

## Development

```bash
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## License

See [LICENSE.txt](LICENSE.txt)
