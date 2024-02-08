import json
import glob
from . import convert
import paramiko
import scp
import math
import os

from data_assets.point import Point
from SplineGeneration import generateSplines

def get_connection(addr: str):
    print("Connecting...")
    try:
        ssh_cli = paramiko.SSHClient()
        ssh_cli.load_system_host_keys()
        ssh_cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cli.connect(addr, username = "lvuser", password = "", timeout = 1)
        scp_cli = scp.SCPClient(ssh_cli.get_transport())
        print("Got connection successfully")
        return scp_cli, ssh_cli
    except TimeoutError:
        print("Connection timed out")
        return
    except:
        print("Error connecting")
        return

def upload_all(addr: str):
    print("Uploading...")
    saves = glob.glob("saves/*.json*")
    conns = get_connection(addr)
    if conns == None:
        return False
    scp_cli = conns[0]
    try:
        for save in saves:
            scp_cli.put(save, remote_path = "/home/lvuser/deploy")
        print("Uploaded all save files")
        scp_cli.close()
        return True
    except:
        return False

def upload(addr: str, file_path: str):
    print("Uploading all...")
    conns = get_connection(addr)
    if conns == None:
        return False
    scp_cli = conns[0]
    try:
        scp_cli.put(file_path, remote_path = "/home/lvuser/deploy")
        print("Uploaded save successfully")
        scp_cli.close()
        return True
    except:
        return False

def download_all(addr: str):
    print("Downloading all...")
    conns = get_connection(addr)
    if conns == None:
        print("Download all failed")
        return False
    scp_cli = conns[0]
    ssh_cli = conns[1]
    try:
        sftp = ssh_cli.open_sftp()
        remote_saves = sftp.listdir("/home/lvuser/deploy")
        for rs in remote_saves:
            if rs.endswith(".json"):
                scp_cli.get(remote_path = f"/home/lvuser/deploy/{rs}", local_path = "saves/")
                print(f"Downloaded {rs}")
        print("Downloaded all saves successfully")
        scp_cli.close()
        ssh_cli.close()
        return True
    except:
        return False

def download_recorded_data(addr: str):
    print("Downloading all recordings...")
    conns = get_connection(addr)
    if conns == None:
        print("Recorded data download failed")
        return False
    scp_cli = conns[0]
    ssh_cli = conns[1]
    sftp = ssh_cli.open_sftp()
    remote_recordings = sftp.listdir("/home/lvuser/deploy/recordings")
    for rr in remote_recordings:
        if rr.endswith(".csv"):
            scp_cli.get(remote_path = f"/home/lvuser/deploy/recordings/{rr}", local_path = "recorded_data/")
            print(f"Downloaded {rr}")
    print("Recorded data downloaded successfully")
    scp_cli.close()
    ssh_cli.close()

def save_path(key_points: list[Point], commands: list, sampled_points: list, sample_rate: float, folder_path: str, file_name: str):
    data = {}
    data["meta_data"] = {
        "path_name": file_name,
        "sample_rate": sample_rate
    }
    data["commands"] = commands
    data["key_points"] = [p.to_json() for p in key_points]
    data["sampled_points"] = [[sampled_points[i][0], sampled_points[i][1], sampled_points[i][2], sampled_points[i][3], sampled_points[i][4], sampled_points[i][5], sampled_points[i][6], sampled_points[i][7]] for i in range(len(sampled_points))]
    try:
        out_file = open(f"{folder_path}\\{file_name}.json", "w")
        json.dump(data, out_file, indent = 2)
        out_file.close()
        print("Path saved successfully")
        return True
    except:
       print("Path was unable to be saved")
       return False

def load_path(file_path: str):
    try:
        with open(file_path) as json_save:
            data = json.load(json_save)
            key_points = []
            for p in data["key_points"]:
                key_points.append(Point(p["index"], p["delta_time"], p["x"], p["y"], p["angle"], p["velocity_magnitude"], p["velocity_theta"], p["angular_velocity"]))
            print("Path loaded successfully")
            return key_points, data["meta_data"]["sample_rate"], data["meta_data"]["path_name"], data["commands"]
    except:
        print("Path was unable to be loaded")
        return [], 0.01, "", []

def clear_local_recordings():
    try:
        recordings = glob.glob("./recorded_data/*")
        for r in recordings:
            os.remove(r)
        print("Cleared all local recordings")
        return True
    except:
        print("Error clearing local recordings")
        return False
    
def clear_rio_recordings(addr: str):
    print("Clearing all recordings on the roborio...")
    conns = get_connection(addr)
    if conns == None:
        print("Clearing roborio recordings failed")
        return False
    scp_cli = conns[0]
    ssh_cli = conns[1]
    sftp = ssh_cli.open_sftp()
    remote_recordings = sftp.listdir("/home/lvuser/deploy/recordings")
    for rr in remote_recordings:
        sftp.remove(f"/home/lvuser/deploy/recordings/{rr}")
    print("Cleared all recordings on the roborio")
    scp_cli.close()
    ssh_cli.close()
    return True