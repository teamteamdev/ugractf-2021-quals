#!/usr/bin/env python3

from flask import Flask, render_template, request, abort, redirect, url_for
import re
import hmac
import sys
import os
import shutil
import tempfile
import subprocess
from werkzeug.utils import secure_filename

from kyzylborda.supervisor.bubblewrap import MountPoint, BubblewrapSpec, bubblewrap_args

PREFIX = "ugra_who_checks_the_checker_"
SECRET2 = b"FXLtTMGeR9MyRyLV"
SALT2_SIZE = 12


def get_flag(token):
    return PREFIX + hmac.new(SECRET2, token.encode(), "sha256").hexdigest()[:SALT2_SIZE]


def make_app():
    app = Flask(__name__)

    @app.route('/<token>/', methods=["GET"])
    def main_get(token):
        return render_template("form.html", success=None)


    def prepare_path(token):
        sandbox_dir = tempfile.TemporaryDirectory(prefix="antivirus")
        try:
            etc_dir = os.path.join(sandbox_dir.name, "etc")
            os.makedirs(etc_dir)
            tmp_dir = os.path.join(sandbox_dir.name, "tmp")
            os.makedirs(tmp_dir)

            with open(os.path.join(etc_dir, "passwd"), "w") as tasks:
                tasks.write(get_flag(token))
            return sandbox_dir
        except:
            sandbox_dir.cleanup()
            raise


    @app.route('/<token>/', methods=["POST"])
    def main_post(token):
        # Just in case.
        if re.fullmatch("[a-zA-Z0-9]+", token) is None:
            abort(500)
        file = request.files["file"]
        ext = request.form["ext"]
        path = prepare_path(token)
        if file.filename != "":
            fname = secure_filename(file.filename)
        else:
            fname = "tmpfile"
        file_path = os.path.join(path.name, "tmp", fname)
        file.save(file_path)
        try:
            bspec = BubblewrapSpec(
                args=[sys.executable, "antivirus.py", ext, f"/tmp/uploads/{fname}"],
                mounts={
                    "/etc": MountPoint(f"{path.name}/etc", read_only=True),
                    "/app": MountPoint("inner_app", read_only=True),
                    "/tmp/uploads": MountPoint(f"{path.name}/tmp"),
                },
                cwd="/app",
            )
            args = bubblewrap_args(bspec)
            ret = subprocess.run(args, stdout=subprocess.PIPE, timeout=10)
        except subprocess.TimeoutExpired:
            return render_template("form.html", success=False, errormsg="Время истекло.")

        path.cleanup()

        if ret.returncode == 0:
            return render_template("form.html", success=True)
        else:
            return render_template("form.html", success=False, errormsg=ret.stdout.decode("utf-8"))


    return app


if __name__ == "__main__":
    app = make_app()
    app.run(host='0.0.0.0', port=31337, debug=True)
