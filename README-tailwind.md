Instalación de Tailwind (offline) para este proyecto

1) Prerrequisitos
- Node.js (>=16) y npm instalados localmente.

2) Instalar dependencias (una vez):

```bash
# desde la raíz del proyecto
npm install
```

Esto descargará `tailwindcss`, `postcss`, `autoprefixer` y `flowbite` en `node_modules`.

3) Construir CSS para producción (genera `static/css/tailwind.css`):

```bash
npm run build:css
```

4) Desarrollo con watch (reconstruye automáticamente):

```bash
npm run watch:css
```

5) Plantillas
- Ya actualicé las plantillas para cargar `{{ url_for('static', filename='css/tailwind.css') }}` en lugar del CDN.

6) Flowbite (opcional offline)
- Si necesitas Flowbite offline, está en `node_modules/flowbite`. Copia el JS a `static/js/flowbite.js` y el CSS está incluido desde `src/styles.css` por la importación.

7) Notas
- El archivo fuente de Tailwind está en `src/styles.css`.
- `tailwind.config.js` incluye las rutas `templates` y `static/js` para purgar clases no usadas.

Si quieres, ejecuto `npm install` aquí (si prefieres), o creo los scripts adicionales para copiar archivos de `node_modules/flowbite` a `static/`.
