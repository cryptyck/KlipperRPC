from discordrp import Presence
from datetime import timedelta
import klipper, yaml, time

with open("config.yaml", "r") as yaml_file:
    config = yaml.safe_load(yaml_file)

printer_ip = config["network"]["printer-ip"]
printer_port = config["network"]["printer-port"]
update_delay = config["rpc"]["update-delay"]
client_id = config["rpc"]["client-id"]

art_assets = {
    "Green": "all-good",
    "Orange": "issue",
    "Red": "failure"
}

with Presence(client_id) as presence:
    print("RPC Connected")

    #TODO: rewrite this entire loop...

    while True:
        print_info = klipper.get_printer_status(printer_ip, printer_port)   
        if print_info["state"] == "printing":
            presence.set(
                {
                    "state": f"Printing {print_info['filename']}",
                    "details": f"{print_info['progresspercent']}% complete!",
                    "timestamps": {"end": round(time.time() + print_info["eta"], 1)},
                    "assets": {
                        "large_image": "klipperlogo",
                        "large_text": f"Nozzle temp: {print_info['nozzletemp']}℃, Bed temp: {print_info['bedtemp']}℃",
                        "small_image": art_assets["Green"],
                        "small_text": "Looking good!",
                    },
                }
            )
        elif print_info["state"] == "standby":
            presence.set(
                {
                    "state": f"On standby...",
                    "assets": {
                        "large_image": "klipperlogo", 
                        "small_image": art_assets["Orange"],
                        "small_text": "Standing by...",
                    },
                }
            )
        elif print_info["state"] == "paused":
            presence.set(
                {
                    "state": f"Paused while printing {print_info['filename']}",
                    "assets": {
                        "large_image": "klipperlogo",
                        "large_text": f"Nozzle temp: {print_info['nozzletemp']}℃, Bed temp: {print_info['bedtemp']}℃",
                        "small_image": art_assets["Orange"],
                        "small_text": "Print paused...",
                    },
                }
            )
        elif print_info["state"] == "complete":
            presence.set(
                {
                    "state": f"Finished printing {print_info['filename']}!",
                    "details": f"Total print time: {print_info['printtime']}",
                    "assets": {
                        "large_image": "klipperlogo",
                        "large_text": f"Nozzle temp: {print_info['nozzletemp']}℃, Bed temp: {print_info['bedtemp']}℃",
                        "small_image": art_assets["Green"],
                        "small_text": "Finished!",
                    },
                }
            )
        elif print_info["state"] == "error":
            presence.set(
                {
                    "state": f"Error!",
                    "details": print_info["statusmessage"],
                    "assets": {
                        "large_image": "klipperlogo",
                        "small_image": art_assets["Red"],
                        "small_text": "An error has occured!",
                    },
                }
            )
        elif print_info["hostonline"] == False:
            presence.set(
                {
                    "state": f"Printer Unreachable.",
                    "details": "Unable to retrieve printer status...",
                    "assets": {
                        "large_image": "klipperlogo",
                        "small_image": art_assets["Red"],
                        "small_text": "Unable to reach printer.",
                    },
                }
            )
        print("Presence updated")
        time.sleep(15)