import streamlit as st

# ==========================================
# 1. BASE DE DATOS EN LA MEMORIA (SESSION STATE)
# ==========================================
# Si es la primera vez que se abre la página, guardamos la lista en la memoria
if 'plantel' not in st.session_state:
    st.session_state.plantel = [
        {"nombre": "Daniel Alvarado", "posicion": "Mediocampista", "goles": 2, "asistencias": 0, "partidos_jugados": 1, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Raúl Ledezma", "posicion": "Defensa", "goles": 0, "asistencias": 0, "partidos_jugados": 1, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Christian Solís", "posicion": "Delantero", "goles": 3, "asistencias": 2, "partidos_jugados": 2, "tarjetas_amarillas": 1, "tarjetas_rojas": 0},
        {"nombre": "Nicolas De la Torre", "posicion": "Mediocampista", "goles": 3, "asistencias": 0, "partidos_jugados": 2, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Bernabe Beltrán", "posicion": "Defensa", "goles": 0, "asistencias": 0, "partidos_jugados": 1, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Donovan Monares", "posicion": "Defensa", "goles": 0, "asistencias": 0, "partidos_jugados": 1, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Arnoldo Segura", "posicion": "Portero", "goles": 0, "asistencias": 0, "partidos_jugados": 2, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Ángel Díaz", "posicion": "Mediocampista", "goles": 0, "asistencias": 0, "partidos_jugados": 1, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Eduardo Morales", "posicion": "Defensa", "goles": 0, "asistencias": 0, "partidos_jugados": 1, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Samuel Dueñas", "posicion": "Delantero", "goles": 4, "asistencias": 1, "partidos_jugados": 2, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Diego Cerda", "posicion": "Delantero", "goles": 4, "asistencias": 0, "partidos_jugados": 2, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Luis Ortega", "posicion": "Delantero", "goles": 4, "asistencias": 1, "partidos_jugados": 2, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Adrián Nuñez", "posicion": "Delantero", "goles": 0, "asistencias": 0, "partidos_jugados": 1, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Enrique González", "posicion": "Mediocampista", "goles": 0, "asistencias": 0, "partidos_jugados": 1, "tarjetas_amarillas": 0, "tarjetas_rojas": 0},
        {"nombre": "Braulio Rodríguez", "posicion": "Mediocampista", "goles": 0, "asistencias": 0, "partidos_jugados": 1, "tarjetas_amarillas": 0, "tarjetas_rojas": 0}
    ]

# ==========================================
# 2. FUNCIONES DEL SISTEMA
# ==========================================
def obtener_tabla_goleadores(lista_jugadores):
    jugadores_ordenados = sorted(lista_jugadores, key=lambda x: x["goles"], reverse=True)
    tabla = []
    for jugador in jugadores_ordenados:
        if jugador["goles"] > 0:
            promedio = round(jugador["goles"] / jugador["partidos_jugados"], 2) if jugador["partidos_jugados"] > 0 else 0.0
            tabla.append({
                "Nombre": jugador["nombre"],
                "Goles": jugador["goles"],
                "Partidos": jugador["partidos_jugados"],
                "Promedio": promedio
            })
    return tabla

def tabla_generadores(lista_jugadores):
    generadores = sorted(lista_jugadores, key=lambda x: x["goles"] + x["asistencias"], reverse=True)
    resumen = []
    for j in generadores:
        total = j["goles"] + j["asistencias"]
        if total > 0:
            resumen.append({"Nombre": j["nombre"], "Goles + Asistencias ": total})
    return resumen

# ==========================================
# 3. INTERFAZ WEB (STREAMLIT)
# ==========================================

st.title(" Estadísticas de Decepción FC")

# --- NUEVO: FORMULARIO DE REGISTRO ---
st.header(" Registrar Partido")
with st.form("registro_estadisticas"):
    st.write("Agrega las estadísticas de hoy para un jugador:")
    
    # Extraemos todos los nombres para hacer un menú desplegable
    nombres_jugadores = [jugador["nombre"] for jugador in st.session_state.plantel]
    jugador_seleccionado = st.selectbox("Selecciona al jugador:", nombres_jugadores)
    
    # Dividimos la pantalla en dos columnas para que se vea más pro
    col1, col2 = st.columns(2)
    goles_hoy = col1.number_input("Goles anotados", min_value=0, value=0)
    asistencias_hoy = col2.number_input("Asistencias", min_value=0, value=0)
    
    # Botón para enviar el formulario
    submit_btn = st.form_submit_button("Guardar Estadísticas")

    # ¿Qué pasa cuando le dan clic al botón?
    if submit_btn:
        for jugador in st.session_state.plantel:
            if jugador["nombre"] == jugador_seleccionado:
                jugador["partidos_jugados"] += 1
                jugador["goles"] += goles_hoy
                jugador["asistencias"] += asistencias_hoy
                st.success(f"¡Estadísticas actualizadas para {jugador_seleccionado}!")

st.divider() # Pone una línea separadora bonita

# --- TABLAS (Leen directamente de la memoria) ---
st.header("Tabla de Goleadores")
# Le pasamos la base de datos de la memoria, no la original
tabla_goles = obtener_tabla_goleadores(st.session_state.plantel)
st.dataframe(tabla_goles, use_container_width=True)

st.header("Participación en Goles (G + A)")
tabla_gen = tabla_generadores(st.session_state.plantel)
st.dataframe(tabla_gen, use_container_width=True)

st.header("Plantel Completo")
st.dataframe(st.session_state.plantel, use_container_width=True)