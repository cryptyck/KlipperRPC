import requests, socket, urllib
from datetime import timedelta

def isOpen(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False

def get_printer_status(printer_ip, printer_port):
    host_online = isOpen(printer_ip, printer_port)
    if host_online:
        # Query printer for objects
        status = requests.get(f"http://{printer_ip}/printer/objects/query?&virtual_sdcard&print_stats").json()
        progress = status["result"]["status"]["virtual_sdcard"]["progress"]
        rounded_progress = round(status["result"]["status"]["virtual_sdcard"]["progress"] * 100)
        print_time = timedelta(seconds=round(status["result"]["status"]["print_stats"]["total_duration"]))
        filename = status["result"]["status"]["print_stats"]["filename"]
        state = status["result"]["status"]["print_stats"]["state"]
        status_message = status["result"]["status"]["print_stats"]["message"]

        # Query printer for file metadata
        metadata = requests.get(f"http://{printer_ip}/server/files/metadata?filename={urllib.parse.quote(filename)}").json()
        if metadata.status_code == 200:
            eta = metadata["result"]["estimated_time"] - (progress * metadata["result"]["estimated_time"])
        else:
            eta = "N/A"

        # Query printer for temps
        temps = requests.get(f"http://{printer_ip}/server/temperature_store?include_monitors=false").json()
        bed_temp = temps["result"]["heater_bed"]["temperatures"][len(temps["result"]["heater_bed"]["temperatures"])-1]
        nozzle_temp = temps["result"]["extruder"]["temperatures"][len(temps["result"]["extruder"]["temperatures"])-1]

        return {
                    "hostonline": host_online,
                    "progresspercent":rounded_progress,
                    "eta": eta,
                    "filename": filename,
                    "bedtemp": bed_temp,
                    "nozzletemp": nozzle_temp,
                    "state": state,
                    "statusmessage": status_message,
                    "printtime": print_time
            }
    else:
        print("KLIPPER WARNING: Printer is unreachable.")
        return {
                    "hostonline": host_online,
                    "progresspercent":"N/A",
                    "eta": "N/A",
                    "filename": "N/A",
                    "bedtemp": "N/A",
                    "nozzletemp": "N/A",
                    "state": "N/A",
                    "statusmessage": "N/A",
                    "printtime": "N/A"
            }