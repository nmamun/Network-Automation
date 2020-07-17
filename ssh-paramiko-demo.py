#!/usr/bin/env python

"""
Author - Nurul Mamun
Version - 1.0
Date - 03 July, 2020
Description - SSH using Paramiko and print it to screen
"""

import time
import paramiko


def send_command(connection, command):
    """
    open connection and send a command,
    issue command and wait 1 second for the command to be processed
    """
    connection.send(command + "\n")
    time.sleep(1.0)


def get_output(connection):
    """
    read all the data from buffer and decode the byte string as UTF-8
    """
    return connection.recv(65535).decode("utf-8")


def main():
    """
    main program
    """
    # declare dictionary for list of hosts and related commands
    host_dict = {
        "R1": "show running-config",
        "R2": "show running-config",
    }
    # iterate over the dictionary items
    for hostname, show_command in host_dict.items():
        # Define paramiko SSH client
        conn_params = paramiko.SSHClient()

        # Adding SSH client parameters, allowing without missing SSH keys
        conn_params.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn_params.connect(
            hostname=hostname,
            port=22,
            username='cisco',
            password='cisco',
            look_for_keys=False,
            allow_agent=False,
        )

    # Get an interactive shell and wait a bit for the prompt to appear
    connection = conn_params.invoke_shell()
    time.sleep(1.0)
    print(f"Logged into {get_output(connection).strip()} successfully")

    # Iterate over the list of commands, sending each one in series
    commands = [
        "terminal length 0",
        "show version | include Software",
        show_command
    ]
    for command in commands:
        send_command(connection, command)
        print(get_output(connection))

    # close connection when done
    connection.close()


if __name__ == "__main__":
    main()
