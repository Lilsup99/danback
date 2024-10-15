# Actividad 1 03/10/2024

En la base de datos de MONGODB (gobernacion_guarico -> homologacion_data) se agrego un campo nuevo que se llama **responsible_entity** Este campo hace referencia a la entidad responsable del proyecto

## 1. Backend (Daniel)

### 1.1 Instrucciones

Se debe agregar esta nueva propiedad a los siguientes endpoint */zone-projs*
y se debe modificar el siguientes archivos

* sinco-data-mapas-dev-f/app/services/v1/query_organization.py:149
* sinco-data-mapas-dev-f/app/services/v1/query_organization.py:302
* sinco-data-mapas-dev-f/app/services/v1/services_project.py:142


## 2. Frontend (Victor)

### 2.2 Instrucciones

Se debe agregar la nueva propiedad a los puntos que se grafican en el mapa y en la tabla los archivos que se deben modificar son los siguientes:

* src/views/dashboard/home/components/MapProj.jsx:196
* src/views/dashboard/home/components/TableProject.jsx:130
