from datetime import datetime, timezone

from airflow import DAG
from airflow.operators.python import PythonOperator
from runtime import run_dbt

with DAG(
    dag_id="examen_ventas",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    max_active_tasks=1,
    default_args={"retries": 0},
    tags=["examen"],
) as dag:
    # dbt source freshness: una advertencia termina con codigo 0 (permite el build);
    # un error termina con codigo distinto de 0, run_dbt lanza la excepcion y la tarea falla.
    verificar_freshness = PythonOperator(
        task_id="verificar_freshness",
        python_callable=run_dbt,
        op_args=[["source", "freshness"]],
    )

    # Regla de ejecucion predeterminada (all_success): si freshness falla,
    # esta tarea queda en upstream_failed y no se ejecuta.
    construir_resumen = PythonOperator(
        task_id="construir_resumen",
        python_callable=run_dbt,
        op_args=[["build"]],
    )

    verificar_freshness >> construir_resumen