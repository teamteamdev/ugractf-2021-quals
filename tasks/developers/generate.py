#!/usr/bin/env python3

import hmac
import json
import subprocess
import tempfile
import os
import random
import shutil
import sys

PREFIX = "ugra_the_yellow_purse_"
SECRET = b"znO3n2w0bAq1LzzD"
SALT_SIZE = 16


def get_flag():
    user_id = sys.argv[1]
    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)
    user_id, target_dir = sys.argv[1], sys.argv[2]
    random.seed(hmac.new(SECRET, str(user_id).encode(), "sha256").digest())

    flag = get_flag()

    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.check_call("git clone https://github.com/edenhill/kafkacat.git", shell=True, cwd=temp_dir)
        git_dir = os.path.join(temp_dir, "kafkacat")

        open(os.path.join(git_dir, ".git", "hooks", "pre-auto-gc"), "w").write('exit 1')
        os.chmod(os.path.join(git_dir, ".git", "hooks", "pre-auto-gc"), 0o755)

        commits = subprocess.check_output("git log | grep '^commit ' | grep -o -E '[0-9a-f]{40}'",
                                          shell=True, cwd=git_dir).decode().strip().split("\n")

        parent_commit = random.choice(commits[-220:-20])
        subprocess.check_call("git checkout " + parent_commit, stdout=subprocess.DEVNULL, shell=True, cwd=git_dir)
        subprocess.check_call(f"""(echo 'If you are reading this, I am definitely dead by now.'; echo;
                                   echo 'I also know that by reaching this file, you have demonstrated';
                                   echo 'the best of your ability and courage. Here is the key to my';
                                   echo 'lifetime secret: {flag}'; echo;
                                   echo 'You will understand what to do next. Good luck!'
                                  ) > info.txt""", stdout=subprocess.DEVNULL, shell=True, cwd=git_dir)

        subprocess.check_call("git add info.txt", shell=True, cwd=git_dir)
        subprocess.check_call("""GIT_AUTHOR_NAME=Validian \\
                                 GIT_AUTHOR_EMAIL=validian@validian.name \\
                                 GIT_AUTHOR_DATE='2019-12-11 06:00:30 +0845' \\
                                 GIT_COMMITTER_NAME=Validian \\
                                 GIT_COMMITTER_EMAIL=validian@validian.name \\
                                 GIT_COMMITTER_DATE='2019-12-11 06:00:30 +0845' \\
                                 git commit -m 'added info.txt.'""", stdout=subprocess.DEVNULL, shell=True, cwd=git_dir)

        subprocess.check_call("git reset --hard " + parent_commit, stdout=subprocess.DEVNULL, shell=True, cwd=git_dir) 
        subprocess.check_call("git checkout " + commits[0], stdout=subprocess.DEVNULL, shell=True, cwd=git_dir) 

        for i in range(9, -1, -1):
            try:
                subprocess.check_call("git reflog delete HEAD@{" + str(i) + "}", shell=True, cwd=git_dir)
            except:
                pass

        subprocess.check_call("zip -r - kafkacat > kafkacat.zip", stdout=subprocess.DEVNULL, shell=True, cwd=temp_dir)
        shutil.copy(os.path.join(temp_dir, "kafkacat.zip"), os.path.join(target_dir, "kafkacat.zip"))

    json.dump({"flags": [flag], "substitutions": {}, "urls": []}, sys.stdout)


if __name__ == "__main__":
    generate()
