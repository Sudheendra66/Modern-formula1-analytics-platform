"""F1 Connector SDK implementation for syncing Drivers, Races, Results, and Standings.
"""

# For reading configuration from a JSON file
import json

# Import required classes from fivetran_connector_sdk
from fivetran_connector_sdk import Connector

# For enabling Logs in your connector code
from fivetran_connector_sdk import Logging as log

# For supporting Data operations like upsert(), update(), delete() and checkpoint()
from fivetran_connector_sdk import Operations as op

# Source-specific imports
from datetime import datetime
from api.drivers import get_drivers
from api.races import get_races
from api.results import get_results
from api.standings import get_standings
from utils.metadata import add_metadata

current_time = datetime.utcnow().isoformat()


def validate_configuration(configuration: dict):
    """
    Validate the configuration dictionary to ensure it contains all required parameters.
    This function is called at the start of the update method to ensure that the connector has all necessary configuration values.
    Args:
        configuration: a dictionary that holds the configuration settings for the connector.
    Raises:
        ValueError: if any required configuration parameter is missing.
    """
    # No mandatory configuration parameters check required for this connector as jolpi api is public.
    pass


def schema(configuration: dict):
    """
    Define the schema function which lets you configure the schema your connector delivers.
    See the technical reference documentation for more details on the schema function:
    https://fivetran.com/docs/connector-sdk/technical-reference/connector-sdk-code/connector-sdk-methods#schema
    Args:
        configuration: a dictionary that holds the configuration settings for the connector.
    """
    return [
        {
            "table": "drivers",
            "primary_key": ["id"],
            "columns": {
                "id": "STRING",
                "name": "STRING",
                "given_name": "STRING",
                "family_name": "STRING",
                "nationality": "STRING"
            },
        },
        {
            "table": "races",
            "primary_key": ["race_id"],
            "columns": {
                "race_id": "STRING",
            },
        },
        {
            "table": "results",
            "primary_key": ["result_id"],
            "columns": {
                "result_id": "STRING",
            },
        },
        {
            "table": "driver_standings",
            "primary_key": ["standing_id"],
            "columns": {
                "standing_id": "STRING",
            },
        },
    ]


def fetch_all_pages(api_func, season, list_extractor):
    """
    Pagination helper that retrieves all pages for a given endpoint and season.
    """
    limit = 100
    offset = 0
    all_items = []

    while True:
        payload = api_func(season=season, limit=limit, offset=offset)
        mr_data = payload.get("MRData", {})
        items = list_extractor(mr_data)
        if not items:
            break

        all_items.extend(items)

        total = int(mr_data.get("total", 0))
        offset += limit
        if offset >= total:
            break

    return all_items


def ingest_drivers(configuration: dict, state: dict, checkpoint_state: dict):
    """
    Ingest drivers data from Jolpica F1 API and upsert into the destination table.
    """
    log.info("Starting drivers ingestion")
    all_drivers = {}
    current_year = datetime.utcnow().year

    for season in range(2020, current_year + 1):
        log.info(f"Fetching drivers for season {season}")
        drivers = fetch_all_pages(
            get_drivers,
            season,
            lambda mr: mr.get("DriverTable", {}).get("Drivers", [])
        )
        for driver in drivers:
            all_drivers[driver["driverId"]] = driver

    for driver in all_drivers.values():
        record = {
            "id": driver["driverId"],
            "name": f"{driver.get('givenName', '')} {driver.get('familyName', '')}",
            "given_name": driver.get("givenName"),
            "family_name": driver.get("familyName"),
            "date_of_birth": driver.get("dateOfBirth"),
            "nationality": driver.get("nationality"),
            "url": driver.get("url"),
            "created_at": current_time,
            "updated_at": current_time
        }
        # Add metadata columns: _loaded_at, _source, _batch_id
        add_metadata(record)
        
        # Upsert driver data
        op.upsert(table="drivers", data=record)

        # Update state tracking for incremental syncs
        record_updated_at = record.get("updated_at")
        if checkpoint_state["last_updated_at"] is None or (
            record_updated_at and record_updated_at > checkpoint_state["last_updated_at"]
        ):
            checkpoint_state["last_updated_at"] = record_updated_at

    log.info(f"Processed {len(all_drivers)} driver record(s)")


def ingest_races(configuration: dict, state: dict, checkpoint_state: dict):
    """
    Ingest races data from Jolpica F1 API and upsert into the destination table.
    """
    log.info("Starting races ingestion")
    all_races = {}
    current_year = datetime.utcnow().year

    for season in range(2020, current_year + 1):
        log.info(f"Fetching races for season {season}")
        races = fetch_all_pages(
            get_races,
            season,
            lambda mr: mr.get("RaceTable", {}).get("Races", [])
        )
        for race in races:
            race_id = f"{race['season']}_{race['round']}"
            all_races[race_id] = race

    for race_id, race in all_races.items():
        circuit = race.get("Circuit", {})
        location = circuit.get("Location", {})
        record = {
            "race_id": race_id,
            "season": race.get("season"),
            "round": race.get("round"),
            "race_name": race.get("raceName"),
            "date": race.get("date"),
            "time": race.get("time"),
            "circuit_id": circuit.get("circuitId"),
            "circuit_name": circuit.get("circuitName"),
            "locality": location.get("locality"),
            "country": location.get("country"),
            "url": race.get("url"),
            "created_at": current_time,
            "updated_at": current_time
        }
        # Add metadata columns: _loaded_at, _source, _batch_id
        add_metadata(record)

        # Upsert race data
        op.upsert(table="races", data=record)

        # Update state tracking for incremental syncs
        record_updated_at = record.get("updated_at")
        if checkpoint_state["last_updated_at"] is None or (
            record_updated_at and record_updated_at > checkpoint_state["last_updated_at"]
        ):
            checkpoint_state["last_updated_at"] = record_updated_at

    log.info(f"Processed {len(all_races)} race record(s)")


def ingest_results(configuration: dict, state: dict, checkpoint_state: dict):
    """
    Ingest race results data from Jolpica F1 API and upsert into the destination table.
    """
    log.info("Starting race results ingestion")
    all_results = {}
    current_year = datetime.utcnow().year

    for season in range(2020, current_year + 1):
        log.info(f"Fetching results for season {season}")
        races = fetch_all_pages(
            get_results,
            season,
            lambda mr: mr.get("RaceTable", {}).get("Races", [])
        )
        for race in races:
            season_num = race.get("season")
            round_num = race.get("round")
            results = race.get("Results", [])

            for result in results:
                driver = result.get("Driver", {})
                driver_id = driver.get("driverId")
                result_id = f"{season_num}_{round_num}_{driver_id}"
                all_results[result_id] = (season_num, round_num, result)

    for result_id, (season_num, round_num, result) in all_results.items():
        driver = result.get("Driver", {})
        constructor = result.get("Constructor", {})
        driver_id = driver.get("driverId")
        
        record = {
            "result_id": result_id,
            "season": season_num,
            "round": round_num,
            "driver_id": driver_id,
            "constructor_id": constructor.get("constructorId"),
            "grid": result.get("grid"),
            "position": result.get("position"),
            "points": result.get("points"),
            "laps": result.get("laps"),
            "status": result.get("status"),
            "created_at": current_time,
            "updated_at": current_time
        }
        # Add metadata columns: _loaded_at, _source, _batch_id
        add_metadata(record)

        # Upsert results data
        op.upsert(table="results", data=record)

        # Update state tracking for incremental syncs
        record_updated_at = record.get("updated_at")
        if checkpoint_state["last_updated_at"] is None or (
            record_updated_at and record_updated_at > checkpoint_state["last_updated_at"]
        ):
            checkpoint_state["last_updated_at"] = record_updated_at

    log.info(f"Processed {len(all_results)} result record(s)")


def ingest_standings(configuration: dict, state: dict, checkpoint_state: dict):
    """
    Ingest standings data from Jolpica F1 API and upsert into the destination table.
    """
    log.info("Starting standings ingestion")
    all_standings = {}
    current_year = datetime.utcnow().year

    for season in range(1950, current_year + 1):
        log.info(f"Fetching standings for season {season}")
        standings_lists = fetch_all_pages(
            get_standings,
            season,
            lambda mr: mr.get("StandingsTable", {}).get("StandingsLists", [])
        )
        for standings_list in standings_lists:
            season_num = standings_list.get("season")
            round_num = standings_list.get("round")
            driver_standings = standings_list.get("DriverStandings", [])

            for standing in driver_standings:
                driver = standing.get("Driver", {})
                driver_id = driver.get("driverId")
                standing_id = f"{season_num}_{round_num}_{driver_id}"
                all_standings[standing_id] = (season_num, round_num, standing)

    for standing_id, (season_num, round_num, standing) in all_standings.items():
        driver = standing.get("Driver", {})
        driver_id = driver.get("driverId")
        
        record = {
            "standing_id": standing_id,
            "season": season_num,
            "round": round_num,
            "driver_id": driver_id,
            "position": standing.get("position"),
            "points": standing.get("points"),
            "wins": standing.get("wins"),
            "created_at": current_time,
            "updated_at": current_time
        }
        # Add metadata columns: _loaded_at, _source, _batch_id
        add_metadata(record)

        # Upsert standings data
        op.upsert(table="driver_standings", data=record)

        # Update state tracking for incremental syncs
        record_updated_at = record.get("updated_at")
        if checkpoint_state["last_updated_at"] is None or (
            record_updated_at and record_updated_at > checkpoint_state["last_updated_at"]
        ):
            checkpoint_state["last_updated_at"] = record_updated_at

    log.info(f"Processed {len(all_standings)} standings record(s)")


def update(configuration: dict, state: dict):
    """
    Define the update function, which is a required function, and is called by Fivetran during each sync.
    See the technical reference documentation for more details on the update function
    https://fivetran.com/docs/connectors/connector-sdk/technical-reference#update
    Args:
        configuration: A dictionary containing connection details
        state: A dictionary containing state information from previous runs
        The state dictionary is empty for the first sync or for any full re-sync
    """
    # Validate the configuration to ensure it contains all required values.
    validate_configuration(configuration=configuration)

    try:
        # Checkpoint state dictionary that holds the last updated timestamp
        checkpoint_state = {"last_updated_at": state.get("last_updated_at")}

        # Perform ingestion for all tables
        ingest_drivers(configuration, state, checkpoint_state)
        ingest_races(configuration, state, checkpoint_state)
        ingest_results(configuration, state, checkpoint_state)
        ingest_standings(configuration, state, checkpoint_state)

        # Update state with the current sync time for the next run
        new_state = {"last_updated_at": checkpoint_state["last_updated_at"]}

        # Save progress by checkpointing
        op.checkpoint(new_state)
        log.info(f"Data synced successfully. Last updated at: {new_state['last_updated_at']}")

    except Exception as e:
        raise RuntimeError(f"Failed to sync data: {str(e)}")


# Create the connector object using the schema and update functions
connector = Connector(update=update, schema=schema)

# Check if the script is being run as the main module.
if __name__ == "__main__":
    # Open the configuration.json file and load its contents
    with open("configuration.json", "r") as f:
        configuration = json.load(f)

    # Test the connector locally
    connector.debug(configuration=configuration)
