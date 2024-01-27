from discordrp import Presence
from datetime import timedelta
import requests
import json
import time
import urllib
import socket

printer_ip = "192.168.1.39" # Printer IP here, probably around 0.39% chance that this is what your printer uses... CHANGE THIS!!!
printer_port = 80   # Default port for HTTP, 99.99% chance that this is what your printer uses by default

update_delay = 15   # 15 seconds is the minimum that Discord allows, IIRC


client_id = "1200689886626332743" # Discord RPC stuff

def isOpen(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False

def get_printer_status():
    hostonline = isOpen(printer_ip, printer_port)
    if hostonline:
        r = requests.get(f"http://{printer_ip}/printer/objects/query?&virtual_sdcard&print_stats")
        print(r)
        r = json.loads(r.text)
        progress = r["result"]["status"]["virtual_sdcard"]["progress"]
        roundedprogress = round(r["result"]["status"]["virtual_sdcard"]["progress"] * 100)
        printtime = timedelta(seconds=round(r["result"]["status"]["print_stats"]["total_duration"]))
        filename = r["result"]["status"]["print_stats"]["filename"]
        state = r["result"]["status"]["print_stats"]["state"]
        statusmessage = r["result"]["status"]["print_stats"]["message"]
        metadatareq = requests.get(f"http://{printer_ip}/server/files/metadata?filename={urllib.parse.quote(filename)}")
        print(metadatareq)
        if metadatareq.status_code == 200:
            metadatareq = json.loads(metadatareq.text)
            eta = metadatareq["result"]["estimated_time"] - (progress * metadatareq["result"]["estimated_time"])
        else:
            eta = "Unavailable"
        tempreq = requests.get(f"http://{printer_ip}/server/temperature_store?include_monitors=false")
        print(tempreq)
        tempreq = json.loads(tempreq.text)
        bedtemp = tempreq["result"]["heater_bed"]["temperatures"][len(tempreq["result"]["heater_bed"]["temperatures"])-1]
        nozzletemp = tempreq["result"]["extruder"]["temperatures"][len(tempreq["result"]["extruder"]["temperatures"])-1]

        return {
                    "hostonline": hostonline,
                    "progresspercent":roundedprogress,
                    "eta": eta,
                    "filename": filename,
                    "bedtemp": bedtemp,
                    "nozzletemp": nozzletemp,
                    "state": state,
                    "statusmessage": statusmessage,
                    "printtime": printtime
            }
    else:
        return {
                    "hostonline": hostonline,
                    "progresspercent":"N/A",
                    "eta": "N/A",
                    "filename": "N/A",
                    "bedtemp": "N/A",
                    "nozzletemp": "N/A",
                    "state": "N/A",
                    "statusmessage": "N/A",
                    "printtime": "N/A"
            }



with Presence(client_id) as presence:
    print("Connected")


    while True:
        print_info = get_printer_status()
        if print_info["state"] == "printing":
            presence.set(
                {
                    "state": f"Printing {print_info['filename']}",
                    "details": f"{print_info['progresspercent']}% complete!",
                    "timestamps": {"end": round(time.time() + print_info["eta"], 1)},
                    "assets": {
                        "large_image": "klipperlogo",
                        "large_text": f"Nozzle temp: {print_info['nozzletemp']}℃, Bed temp: {print_info['bedtemp']}℃",
                        "small_image": "all-good",
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
                        "small_image": "issue",
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
                        "small_image": "issue",
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
                        "small_image": "all-good",
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
                        "small_image": "failure",
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
                        "small_image": "failure",
                        "small_text": "Unable to reach printer.",
                    },
                }
            )
        print("Presence updated")
        time.sleep(15)