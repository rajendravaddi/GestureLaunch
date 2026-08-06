import os
import shlex
import subprocess


def launch_application(exec_command: str) -> bool:
    """Launches an application as a detached background process."""
    if not exec_command.strip():
        return False

    try:
        # Detach subprocess so it keeps running independently
        subprocess.Popen(
            exec_command,
            shell=True,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception as e:
        print(f"[Launcher Error] Failed to launch '{exec_command}': {e}")
        return False
