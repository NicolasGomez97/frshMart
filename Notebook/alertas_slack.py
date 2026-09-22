# alertas_slack.py -- Ejemplo de como se integraria con Slack
import requests
from datetime import date


def enviar_alerta_slack(webhook_url: str, gaps: list[date]):
    """
    Envia una alerta a Slack cuando hay dias sin datos.
    En un entorno real, el webhook_url seria una variable de entorno.
    """
    if not gaps:
        return  # No hay gaps, no alertar

    fechas_str = ", ".join(f.strftime("%Y-%m-%d") for f in gaps)
    mensaje = {
        "text": (
            f":warning: *ALERTA: Pipeline sin datos*\n"
            f"Dias afectados: {fechas_str}\n"
            f"Total gaps: {len(gaps)} dia(s)\n"
            f"Accion: revisar DAG 'raw_to_gold_ventas' en Airflow"
        )
    }

    response = requests.post(webhook_url, json=mensaje)
    if response.status_code == 200:
        print(f"Alerta enviada a Slack: {len(gaps)} gap(s) detectado(s)")
    else:
        print(f"Error enviando alerta: {response.status_code}")


# En produccion esto iria en un DAG de Airflow que corre a las 7:00 AM
# O en un cron job: 0 7 * * * python alertas_slack.py