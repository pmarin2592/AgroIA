import streamlit as st

from src.train.ann import ann
from src.utils.metrics import obtener_ruta_app

class Modulo3Web:
    def __init__(self):
        # Crear instancia del recomendador climático
        self.modelo_ann = ann(obtener_ruta_app("AgroIA"))

    def render(self):
        st.set_page_config(
            page_title='Recomendación de acción',
            layout='wide',
            initial_sidebar_state='expanded'
        )

        st.title('AgroIA: Asistente Inteligente para el cultivo de la papa en Cartago, Costa Rica')

        st.write("""
        **AgroIA** ofrece recomendaciones para el manejo de cultivos, basadas en condiciones climáticas y del suelo.
        """)

        self.mostrar_predicciones()

    def interpretar_recomendacion(self,recomendacion):
        """
        Muestra la interpretación de cada recomendación
        """
        interpretaciones = {
            'riego': {
                'emoji': '💧',
                'titulo': 'Riego Necesario',
                'descripcion': 'Las condiciones indican que el cultivo necesita riego adicional.',
                'acciones': ['Aumentar frecuencia de riego', 'Verificar humedad del suelo',
                             'Monitorear plantas por signos de estrés hídrico']
            },
            'fertilizacion': {
                'emoji': '🌱',
                'titulo': 'Fertilización Recomendada',
                'descripcion': 'El cultivo requiere nutrientes adicionales para un crecimiento óptimo.',
                'acciones': ['Aplicar fertilizante apropiado', 'Verificar pH del suelo',
                             'Considerar fertilizantes orgánicos']
            },
            'poda_preventiva': {
                'emoji': '✂️',
                'titulo': 'Poda Preventiva',
                'descripcion': 'Se recomienda realizar poda preventiva para mantener la salud del cultivo.',
                'acciones': ['Podar partes enfermas o dañadas', 'Mejorar circulación de aire',
                             'Prevenir propagación de enfermedades']
            }
        }

        info = interpretaciones.get(recomendacion, {
            'emoji': '❓',
            'titulo': 'Recomendación Desconocida',
            'descripcion': 'No se pudo interpretar la recomendación.',
            'acciones': ['Consultar con un experto']
        })

        # Mostrar con estilo
        st.info(f"{info['emoji']} **{info['titulo']}**")
        st.write(info['descripcion'])

        st.write("**Acciones recomendadas:**")
        for accion in info['acciones']:
            st.write(f"• {accion}")

    def mostrar_predicciones(self):
        st.subheader('Ingrese los datos')

        # Inputs para las predicciones
        temperatura = st.number_input('Temperatura máxima (°C)', min_value=0, max_value=50)
        temperatura_min = st.number_input('Temperatura minima (°C)', min_value=0, max_value=50)
        humedad_aire = st.number_input('Humedad del aire (%)', min_value=0, max_value=100)
        precipitacion = st.number_input('Precipitación (mm)', min_value=0, max_value=1000)
        ph_suelo = st.number_input('pH del suelo', min_value=0.0, max_value=14.0)


        # Botón para generar recomendación
        if st.button('Obtener Recomendación'):
            try:
                # Crear fila con los datos
                fila = {
                    "lluvia_mm": precipitacion,
                    "temp_max": temperatura,
                    "temp_min": temperatura_min,
                    "humedad": humedad_aire,
                    "ph_suelo": ph_suelo
                }


                # Generar predicción de enfermedad
                prediccion_info = self.modelo_ann.predecir_desde_fila(fila)

                """
                    Muestra los resultados de una predicción individual
                    """
                st.subheader("🎯 Resultado de la Predicción")

                # Crear columnas para mostrar información
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Recomendación", prediccion_info['prediccion'])

                with col2:
                    st.metric("Probabilidad", f"{prediccion_info['probabilidad_porcentaje']}%")

                with col3:
                    st.metric("Índice", prediccion_info['indice'])

                # Mostrar barra de progreso de confianza
                st.write("**Nivel de confianza:**")


                # Mostrar interpretación de la recomendación
                self.interpretar_recomendacion(prediccion_info['prediccion'])


            except Exception as e:
                st.error(f"Error: {str(e)}")


