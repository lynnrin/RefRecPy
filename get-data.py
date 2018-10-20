import subprocess
import csv
import os
import glob
from git import *


def rename(home, target, target_file):
    try:
        f_n = glob.glob(home + target_file + "/metric*")
        file_name = home + "lab-test/" + target_file + "/data/" + target + ".xml"
        rename = "mv " + f_n[0] + " " + file_name
        subprocess.run(rename, shell=True)
        return True
    except:
        return False

def play_jar():
    num = 1
    prev_line = "CommitID"
    target_file = "ant"
    home = "/Users/lynn/"
    jar_cmd = ["java", "-jar", home + "jxmetrics/org.jtool.jxmetrics/releases/jxmetrics-1.0-all.jar", "-target", home + target_file  + "/", "-name", "metric"]
    repo = Repo(home + target_file) 
    
    with open(home + "lab-test/" + target_file + "/all_refactorings.csv", "r") as f:
        next(f)
        for line in f:
            line = line.rstrip('\n').split('#')
            if prev_line != line[0]:
                for parentCommit in repo.iter_commits(line[0], max_count=1):
                    print("Start Reset")
                    repo.git.reset('--hard', parentCommit.parents[0])
                    print("Done Reset and Start Jar")
                    subprocess.run(jar_cmd)
                    if rename(home, line[0], target_file):
                        print("Done, " + str(num) + "files")
                        num = num + 1
                prev_line = line[0]

if __name__ == "__main__":
    play_jar()