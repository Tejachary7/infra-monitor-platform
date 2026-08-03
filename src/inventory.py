from pathlib import Path
import yaml


def load_inventory():
    """
    Load the server inventory from inventory/servers.yaml.

    Returns:
        list: List of server dictionaries.
    """

    inventory_path = (
        Path(__file__).resolve().parent.parent
        / "inventory"
        / "servers.yaml"
    )

    try:
        with open(inventory_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return data.get("servers", [])

    except FileNotFoundError:
        print(f"ERROR: Inventory file not found: {inventory_path}")
        return []

    except yaml.YAMLError as error:
        print(f"YAML Error: {error}")
        return []