#!/usr/bin/env python
"""
Update temp_user_files/docker_json_vars.json and Outputfolder/inputs/ so your
interactive container uses the JSON you want. Run this from the docker/ directory.

Usage:
  python update_docker_json_only.py -j .\examples\sample_autogrow_paper_large_scale_trial.json

Then start your interactive container; it will see the updated /UserFiles/docker_json_vars.json.
"""
import argparse
import json
import os
import shutil

def main():
    parser = argparse.ArgumentParser(description="Update docker_json_vars.json and inputs for interactive container.")
    parser.add_argument("-j", "--json", required=True, dest="json_file", help="Path to your JSON config (e.g. .\\examples\\sample_autogrow_paper_large_scale_trial.json)")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(os.getcwd()) != script_dir:
        print(f"Run this script from: {script_dir}")
        print("  cd " + script_dir)
        return 1

    json_path = os.path.abspath(args.json_file)
    if not os.path.isfile(json_path):
        print(f"JSON file not found: {json_path}")
        return 1

    with open(json_path) as f:
        json_vars = json.load(f)

    root = json_vars.get("root_output_folder", "./Outputfolder/")
    root = os.path.abspath(root)
    inputs_dir = os.path.join(root, "inputs")
    os.makedirs(inputs_dir, exist_ok=True)

    receptor = json_vars.get("filename_of_receptor")
    source = json_vars.get("source_compound_file")
    if receptor:
        receptor = os.path.abspath(receptor)
        if os.path.isfile(receptor):
            shutil.copy2(receptor, os.path.join(inputs_dir, os.path.basename(receptor)))
        json_vars["filename_of_receptor"] = "/Outputfolder/inputs/" + os.path.basename(receptor)
    if source:
        source = os.path.abspath(source)
        if os.path.isfile(source):
            shutil.copy2(source, os.path.join(inputs_dir, os.path.basename(source)))
        json_vars["source_compound_file"] = "/Outputfolder/inputs/" + os.path.basename(source)

    json_vars["root_output_folder"] = "/Outputfolder/"
    json_vars["mgltools_directory"] = "/mgltools_x86_64Linux2_1.5.6"
    json_vars["obabel_path"] = "/usr/bin/obabel"

    temp_dir = os.path.join(script_dir, "temp_user_files")
    os.makedirs(temp_dir, exist_ok=True)
    out_path = os.path.join(temp_dir, "docker_json_vars.json")
    with open(out_path, "w") as f:
        json.dump(json_vars, f, indent=4)
    print(f"Updated {out_path}")
    print("Start your interactive container; it will use this JSON.")
    return 0

if __name__ == "__main__":
    exit(main())
