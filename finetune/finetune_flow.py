from __future__ import annotations
from prefect import flow, task, get_run_logger

import os
import json
import numpy as np
import pandas as pd


# Appends a new row to finetune.csv and returns the new count of rows.
@task(log_prints=True)
def append_finetune_row(
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float,
        expected_class_name: str,
        classes_path: str = "data/classes.json",
        finetune_path: str = "data/finetune.csv",
) -> int:
    logger = get_run_logger()

    # Load class name and find its index in the classes.json
    if not os.path.exists(classes_path):
        raise FileNotFoundError(f"Nem található classes.json: {classes_path}")
    with open(classes_path, "r", encoding="utf-8") as f:
        class_names = json.load(f)
    if expected_class_name not in class_names:
        raise ValueError(
            f"Ismeretlen osztálynév: {expected_class_name}. Ismert: {class_names}"
        )
    label_idx = int(class_names.index(expected_class_name))

    # Create a new row
    row = np.array([[sepal_length, sepal_width, petal_length, petal_width, label_idx]])

    os.makedirs(os.path.dirname(finetune_path), exist_ok=True)
    should_read_existing = os.path.exists(finetune_path) and os.path.getsize(finetune_path) > 0

    if should_read_existing:
        try:
            df_existing = pd.read_csv(finetune_path, header=None)
            new_df = pd.concat([df_existing, pd.DataFrame(row)], ignore_index=True)
        except pd.errors.EmptyDataError:
            # Ha mégis üresnek látja, kezdjen új fájlként
            new_df = pd.DataFrame(row)
    else:
        new_df = pd.DataFrame(row)

    new_df.to_csv(finetune_path, index=False, header=False)
    count = len(new_df)
    logger.info(f"Új minta hozzáadva a finetune.csv-hez. Aktuális elemszám: {count}")
    return count


# If count is a multiple of threshold, run finetune.py main()
@task(log_prints=True)
def maybe_run_finetune(count: int, threshold: int = 5) -> bool:
    logger = get_run_logger()
    if count > 0 and (count % threshold == 0):
        logger.info(f"Elérte a küszöböt ({count} = k*{threshold}), finomhangolás indul...")
        import finetune as ft
        ft.finetune_model()
        logger.info("Finomhangolás befejezve.")
        return True
    else:
        logger.info(f"Még nincs küszöbön (count={count}, threshold={threshold}).")
        return False


# Prefect flow definition
@flow(name="Iris Finetune Ingest")
def finetune_ingest_flow(
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float,
        expected_class_name: str,
        threshold: int = 5,
        classes_path: str = "data/classes.json",
        finetune_path: str = "data/finetune.csv",
) -> dict:
    logger = get_run_logger()
    count = append_finetune_row(
        sepal_length,
        sepal_width,
        petal_length,
        petal_width,
        expected_class_name,
        classes_path,
        finetune_path,
    )
    triggered = maybe_run_finetune(count, threshold)
    logger.info(f"Finetune triggered? {triggered}")
    return {"finetune_count": count, "triggered": bool(triggered)}


# Register deployment to Prefect Server
if __name__ == "__main__":
    finetune_ingest_flow.serve(
        name="iris-finetune-ingest",
        tags=["mlops", "iris"],
    )
