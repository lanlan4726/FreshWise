"""Historical forecast snapshots for the public demo; no local CSVs required."""
import json
import math
from pathlib import Path
from freshwise.application_tools import PlanningContext

ROOT = Path(__file__).resolve().parent

def snapshot():
    return json.loads((ROOT / 'demo_forecasts.json').read_text())

def demo_context(center_id, meal_id):
    for row in snapshot()['contexts']:
        record = row['forecast_record']
        if record['center_id'] != center_id or record['meal_id'] != meal_id:
            continue
        if not math.isfinite(row['forecast']) or row['forecast'] < 0:
            raise ValueError('Invalid snapshot forecast')
        if record['history_end_week'] >= record['target_week']:
            raise ValueError('Invalid snapshot chronology')
        return PlanningContext(row['key'], row['forecast'],
            'HISTORICAL DEMO SNAPSHOT: ' + row['source'], forecast_record=record)
    raise ValueError('Choose one of the four supported demo meals at centre 13.')
