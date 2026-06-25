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


def safe_int(value):
    """Safely convert value to int, return None if conversion fails or value is None."""
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def safe_float(value):
    """Safely convert value to float, return None if conversion fails or value is None."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


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
                "date_of_birth": "STRING",
                "nationality": "STRING",
                "url": "STRING",
                "created_at": "STRING",
                "updated_at": "STRING",
                "_loaded_at": "STRING",
                "_source": "STRING",
                "_batch_id": "STRING"
            },
        },
        {
            "table": "races",
            "primary_key": ["race_id"],
            "columns": {
                "race_id": "STRING",
                "season": "INT",
                "round": "INT",
                "race_name": "STRING",
                "date": "STRING",
                "time": "STRING",
                "circuit_id": "STRING",
                "circuit_name": "STRING",
                "locality": "STRING",
                "country": "STRING",
                "url": "STRING",
                "created_at": "STRING",
                "updated_at": "STRING",
                "_loaded_at": "STRING",
                "_source": "STRING",
                "_batch_id": "STRING"
            },
        },
        {
            "table": "results",
            "primary_key": ["result_id"],
            "columns": {
                "result_id": "STRING",
                "season": "INT",
                "round": "INT",
                "driver_id": "STRING",
                "constructor_id": "STRING",
                "grid": "INT",
                "position": "INT",
                "points": "FLOAT",
                "laps": "INT",
                "status": "STRING",
                "created_at": "STRING",
                "updated_at": "STRING",
                "_loaded_at": "STRING",
                "_source": "STRING",
                "_batch_id": "STRING"
            },
        },
        {
            "table": "driver_standings",
            "primary_key": ["standing_id"],
            "columns": {
                "standing_id": "STRING",
                "season": "INT",
                "round": "INT",
                "driver_id": "STRING",
                "position": "INT",
                "points": "FLOAT",
                "wins": "INT",
                "created_at": "STRING",
                "updated_at": "STRING",
                "_loaded_at": "STRING",
                "_source": "STRING",
                "_batch_id": "STRING"
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

    log.info(f"DEBUG: ingest_drivers range: 1970 to {current_year} (inclusive)")
    first_season_processed = None
    last_season_processed = None
    records_per_season = {}

    for season in range(1970, current_year + 1):
        log.info(f"Fetching drivers for season {season}")
        drivers = fetch_all_pages(
            get_drivers,
            season,
            lambda mr: mr.get("DriverTable", {}).get("Drivers", [])
        )
        if first_season_processed is None:
            first_season_processed = season
        last_season_processed = season
        records_per_season[season] = len(drivers)
        
        for driver in drivers:
            all_drivers[driver["driverId"]] = driver
        
        if season in [1970, 1980, 1990, 2000, 2010, 2020, 2026]:
            log.info(f"DEBUG: Season {season} - fetched {len(drivers)} driver records from API")

    log.info(f"DEBUG: First season: {first_season_processed}, Last season: {last_season_processed}")
    log.info(f"DEBUG: Total unique drivers collected: {len(all_drivers)}")

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
    log.info(f"DEBUG: Drivers checkpoint_state after: {checkpoint_state}")
    if first_season_processed is not None:
        log.info(f"✓ DRIVERS: Seasons {first_season_processed}–{last_season_processed} | Total records: {len(all_drivers)}")



def ingest_races(configuration: dict, state: dict, checkpoint_state: dict):
    """
    Ingest races data from Jolpica F1 API and upsert into the destination table.
    """
    log.info("Starting races ingestion")
    all_races = {}
    current_year = datetime.utcnow().year

    log.info(f"DEBUG: ingest_races range: 1970 to {current_year} (inclusive)")
    first_season_processed = None
    last_season_processed = None

    for season in range(1970, current_year + 1):
        log.info(f"Fetching races for season {season}")
        races = fetch_all_pages(
            get_races,
            season,
            lambda mr: mr.get("RaceTable", {}).get("Races", [])
        )
        if first_season_processed is None:
            first_season_processed = season
        last_season_processed = season
        
        for race in races:
            race_id = f"{race['season']}_{race['round']}"
            all_races[race_id] = race
        
        if season in [1970, 1980, 1990, 2000, 2010, 2020, 2026]:
            log.info(f"DEBUG: Season {season} - fetched {len(races)} race records from API")

    log.info(f"DEBUG: First season: {first_season_processed}, Last season: {last_season_processed}")
    log.info(f"DEBUG: Total races collected: {len(all_races)}")

    for race_id, race in all_races.items():
        circuit = race.get("Circuit", {})
        location = circuit.get("Location", {})
        record = {
            "race_id": race_id,
            "season": safe_int(race.get("season")),
            "round": safe_int(race.get("round")),
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
    log.info(f"DEBUG: Races checkpoint_state after: {checkpoint_state}")
    if first_season_processed is not None:
        log.info(f"✓ RACES: Seasons {first_season_processed}–{last_season_processed} | Total records: {len(all_races)}")



def ingest_results(configuration: dict, state: dict, checkpoint_state: dict):
    """
    Ingest race results data from Jolpica F1 API and upsert into the destination table.
    """
    log.info("Starting race results ingestion")
    all_results = {}
    current_year = datetime.utcnow().year

    log.info(f"DEBUG: ingest_results range: 1970 to {current_year} (inclusive)")
    first_season_processed = None
    last_season_processed = None

    for season in range(1970, current_year + 1):
        log.info(f"Fetching results for season {season}")
        races = fetch_all_pages(
            get_results,
            season,
            lambda mr: mr.get("RaceTable", {}).get("Races", [])
        )
        if first_season_processed is None:
            first_season_processed = season
        last_season_processed = season
        
        for race in races:
            season_num = race.get("season")
            round_num = race.get("round")
            results = race.get("Results", [])

            for result in results:
                driver = result.get("Driver", {})
                driver_id = driver.get("driverId")
                result_id = f"{season_num}_{round_num}_{driver_id}"
                all_results[result_id] = (season_num, round_num, result)
        
        if season in [1970, 1980, 1990, 2000, 2010, 2020, 2026]:
            log.info(f"DEBUG: Season {season} - fetched {len(races)} race records with results from API")

    log.info(f"DEBUG: First season: {first_season_processed}, Last season: {last_season_processed}")
    log.info(f"DEBUG: Total result records collected: {len(all_results)}")

    for result_id, (season_num, round_num, result) in all_results.items():
        driver = result.get("Driver", {})
        constructor = result.get("Constructor", {})
        driver_id = driver.get("driverId")
        
        record = {
            "result_id": result_id,
            "season": safe_int(season_num),
            "round": safe_int(round_num),
            "driver_id": driver_id,
            "constructor_id": constructor.get("constructorId"),
            "grid": safe_int(result.get("grid")),
            "position": safe_int(result.get("position")),
            "points": safe_float(result.get("points")),
            "laps": safe_int(result.get("laps")),
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
    log.info(f"DEBUG: Results checkpoint_state after: {checkpoint_state}")
    if first_season_processed is not None:
        log.info(f"✓ RESULTS: Seasons {first_season_processed}–{last_season_processed} | Total records: {len(all_results)}")



def ingest_standings(configuration: dict, state: dict, checkpoint_state: dict):
    """
    Ingest standings data from Jolpica F1 API and upsert into the destination table.
    """
    log.info("Starting standings ingestion")
    all_standings = {}
    current_year = datetime.utcnow().year

    log.info(f"DEBUG: ingest_standings range: 1970 to {current_year} (inclusive)")
    log.info(f"DEBUG: checkpoint_state at start: {checkpoint_state}")
    
    first_season_processed = None
    last_season_processed = None
    records_per_season = {}

    for season in range(1970, current_year + 1):
        log.info(f"Fetching standings for season {season}")
        standings_lists = fetch_all_pages(
            get_standings,
            season,
            lambda mr: mr.get("StandingsTable", {}).get("StandingsLists", [])
        )
        
        season_record_count = 0
        if first_season_processed is None:
            first_season_processed = season
        last_season_processed = season
        
        # DEBUG: Print standings_lists count for specific years
        if season in [1970, 1980, 1990, 2000, 2010, 2020]:
            log.info(f"DEBUG: Season {season} - API returned {len(standings_lists)} standings_lists")
        
        for idx, standings_list in enumerate(standings_lists):
            season_num = standings_list.get("season")
            round_num = standings_list.get("round")
            driver_standings = standings_list.get("DriverStandings", [])

            for standing in driver_standings:
                driver = standing.get("Driver", {})
                driver_id = driver.get("driverId")
                standing_id = f"{season_num}_{round_num}_{driver_id}"
                all_standings[standing_id] = (season_num, round_num, standing)
                season_record_count += 1
                
                # DEBUG: Print first 5 records from 1970
                if season == 1970 and season_record_count <= 5:
                    log.info(f"DEBUG: Season 1970 record {season_record_count}: standing_id={standing_id}, season_num={season_num}, round_num={round_num}")
        
        records_per_season[season] = season_record_count
        if season in [1970, 1980, 1990, 2000, 2010, 2020, 2026]:
            log.info(f"DEBUG: Season {season} - fetched {season_record_count} standing records from API")

    log.info(f"DEBUG: First season processed: {first_season_processed}, Last season processed: {last_season_processed}")
    log.info(f"DEBUG: Total standing records collected: {len(all_standings)}")
    sample_1970_ids = [sid for sid in all_standings.keys() if sid.startswith('1970_')][:3]
    sample_2020_ids = [sid for sid in all_standings.keys() if sid.startswith('2020_')][:3]
    log.info(f"DEBUG: Sample standing_ids from 1970: {sample_1970_ids}")
    log.info(f"DEBUG: Sample standing_ids from 2020: {sample_2020_ids}")
    log.info(f"DEBUG: Attempting driver_standings upsert for {len(all_standings)} records")

    # DEBUG: Before any upserts, analyze all_standings
    if all_standings:
        seasons_in_standings = set(int(sid.split('_')[0]) for sid in all_standings.keys())
        min_season = min(seasons_in_standings)
        max_season = max(seasons_in_standings)
        log.info(f"DEBUG: BEFORE UPSERTS - all_standings contains {len(all_standings)} total records")
        log.info(f"DEBUG: BEFORE UPSERTS - season range in all_standings: {min_season} to {max_season}")
        log.info(f"DEBUG: BEFORE UPSERTS - unique seasons in all_standings: {sorted(list(seasons_in_standings))}")
        
        # Count by decade
        decade_counts = {}
        for s in seasons_in_standings:
            decade = (s // 10) * 10
            if decade not in decade_counts:
                decade_counts[decade] = 0
            decade_counts[decade] += 1
        log.info(f"DEBUG: BEFORE UPSERTS - records by decade: {sorted(decade_counts.items())}")
    else:
        log.info(f"DEBUG: BEFORE UPSERTS - all_standings is EMPTY!")

    for standing_id, (season_num, round_num, standing) in all_standings.items():
        driver = standing.get("Driver", {})
        driver_id = driver.get("driverId")
        
        record = {
            "standing_id": standing_id,
            "season": safe_int(season_num),
            "round": safe_int(round_num),
            "driver_id": driver_id,
            "position": safe_int(standing.get("position")),
            "points": safe_float(standing.get("points")),
            "wins": safe_int(standing.get("wins")),
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
    log.info(f"DEBUG: Final checkpoint_state: {checkpoint_state}")
    if first_season_processed is not None:
        log.info(f"✓ STANDINGS: Seasons {first_season_processed}–{last_season_processed} | Total records: {len(all_standings)}")
    
    # Count records by season decade for verification
    standings_by_season = {}
    for standing_id in all_standings.keys():
        season_from_id = int(standing_id.split('_')[0])
        if season_from_id not in standings_by_season:
            standings_by_season[season_from_id] = 0
        standings_by_season[season_from_id] += 1
    
    log.info(f"DEBUG: Records by season - 1970s: {sum(v for k, v in standings_by_season.items() if 1970 <= k < 1980)}, "
             f"1980s: {sum(v for k, v in standings_by_season.items() if 1980 <= k < 1990)}, "
             f"1990s: {sum(v for k, v in standings_by_season.items() if 1990 <= k < 2000)}, "
             f"2000s: {sum(v for k, v in standings_by_season.items() if 2000 <= k < 2010)}, "
             f"2010s: {sum(v for k, v in standings_by_season.items() if 2010 <= k < 2020)}, "
             f"2020s: {sum(v for k, v in standings_by_season.items() if 2020 <= k < 2030)}")



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
    
    log.info("="*80)
    log.info("ACTIVE CONNECTOR VERSION: 1970-2026 (Historical Data Full Sync)")
    log.info("="*80)
    log.info(f"DEBUG: update() called with state: {state}")

    try:
        # Checkpoint state dictionary that holds the last updated timestamp
        checkpoint_state = {"last_updated_at": state.get("last_updated_at")}
        
        log.info(f"DEBUG: checkpoint_state initialized: {checkpoint_state}")

        # Perform ingestion for all tables
        ingest_drivers(configuration, state, checkpoint_state)
        ingest_races(configuration, state, checkpoint_state)
        ingest_results(configuration, state, checkpoint_state)
        ingest_standings(configuration, state, checkpoint_state)

        # Update state with the current sync time for the next run
        new_state = {"last_updated_at": checkpoint_state["last_updated_at"]}
        
        log.info(f"DEBUG: new_state before checkpoint: {new_state}")

        # Save progress by checkpointing
        op.checkpoint(new_state)
        log.info("="*80)
        log.info("✓ DATA SYNCED SUCCESSFULLY - Historical data (1970-2026) ingested")
        log.info("="*80)
        log.info(f"Last updated at: {new_state['last_updated_at']}")
        log.info(f"DEBUG: Checkpoint saved with state: {new_state}")

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
