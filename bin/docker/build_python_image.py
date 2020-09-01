import argparse
import os
import subprocess
import sys



def _find_workspace():
    result = os.path.abspath(os.path.dirname(__file__))
    while result != "/":
        result = os.path.abspath(os.path.dirname(result))
        if os.path.exists(os.path.join(result, "LICENSE")):
            return result
    return None


class MyWorkSpace:

    def __init__(self, custom_workspace=None):
        if custom_workspace:
            self.workspace = custom_workspace
        else:
            self.workspace = _find_workspace()


def create_command_parser() -> argparse.Namespace:
    result = argparse.ArgumentParser(description='manual to this script')
    result.add_argument('--workspace', type=str, default=None)
    result.add_argument('--app', type=str, default="simple_app")
    return result.parse_args()

if __name__ == '__main__':
    args = create_command_parser()
    workspace = MyWorkSpace(args.workspace)
    print("workspace is {}".format(workspace.workspace))
    commands = ["bin/docker-image-tool.sh",
                 "-t",
                 "v1",
                 "-r",
                 "jyt_spark",
                 "-p",
                 "kubernetes/dockerfiles/spark/bindings/python/Dockerfile",
                 "build"]
    out = subprocess.run(commands, cwd=workspace.workspace)

    if out.returncode !=0:
        print("build failed!!!")
        sys.exit(-1)

    commands = ["docker","tag","jyt_spark/spark-py:v1","localhost:8082/spark:v1"]
    subprocess.run(commands, cwd=workspace.workspace)
    ## need manully login before
    commands = ["docker","push","localhost:8082/spark:v1"]
    subprocess.run(commands, cwd=workspace.workspace)
    commands = ["minikube","ssh"]
    """
    minikube_process = subprocess.Popen(commands,
                               stdin=subprocess.PIPE, 
                               stdout = subprocess.PIPE)
    """
