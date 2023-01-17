#!/usr/bin/python3.8

import http.client
import yaml
import json


def open_var_file(file_name):
    try:
        file = open(file_name, "r")
        return file
    except FileNotFoundError:
        print("File not found")
        exit(1)


def create_env_var(env_name, env_value):

    payload = json.dumps({"name": env_name, "value": env_value})

    conn.request(
        "POST",
        f"/api/v2/project/gh/sambatech/{circleci_project}/envvar",
        payload,
        headers,
    )
    res = conn.getresponse()
    data = res.read()
    status = res.status

    if status in [200, 201]:
        print("Variable name " + env_name + " was created successfully")
    else:
        print(
            "There was a problem creating the variable " + env_name + ": " + str(status)
        )
        print(data.decode("utf-8"))


def define_env_vars(file):
    for line in file:

        env_name, env_value = line.split("=", 1)

        create_env_var(env_name.strip(), env_value.strip())


def main():
    global conn, headers, config, circleci_project

    with open("config.yml", "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.SafeLoader)

    circleci_project = config["CIRCLE_PROJECT"]

    print("Creating environment variables for project " + circleci_project)

    conn = http.client.HTTPSConnection("circleci.com")

    headers = {
        "content-type": "application/json",
        "Circle-Token": config["CIRCLE_PERSONAL_TOKEN"],
    }

    fin = open_var_file("env_vars.txt")

    print("Defining environment variables\n")

    define_env_vars(fin)

    print(f"\n----- Finished execution -----")


if __name__ == "__main__":
    main()
