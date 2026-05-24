# Integrantes del grupo
- Joaquin Arenas Riveros
- Piero Coaguila Sanchez
- Adriano Guetat Concha


## Entidades del modelo

	1. empresa_transporte (Independiente)
	2. terminal (Independiente)
	3. bus (Depende de empresa_transporte y terminal)
	4. ubicacion_bus (Depende de bus)
	5. ruta (Depende de empresa_transporte)
	6. centro_control (Independiente)
	7. pasajero (Independiente)
	8. conductor (Independiente)
	9. notificacion (Depende de centro_control y pasajero)
	10. paradero (Independiente)
	11. recorrido_ruta (Depende de ruta y paradero)
	12. horario (Depende de ruta)
	13. asignacion_conductor (Depende de conductor y bus)
	14. incidencia (Depende de centro_control, pasajero y bus)
	15. registro_control (Depende de bus y centro_control)



