from argparse import ArgumentParser
import os
import tempfile
import shutil
import subprocess
import json
import glob

def main():
    parser = ArgumentParser()
    parser.add_argument('-t', '--template', type=str, required=True, help='name of input latex template file')
    args = parser.parse_args()

    forms = []
    for file in glob.glob("*.json"):
        forms.append(file)

    for form in forms:
        with open(form, "r") as f:
            data = json.load(f)

        lines = []
        counter = 1
        with open(args.template, "r") as f:
            for i, line in enumerate(f):
                if "{x}" in line:
                    line = line.replace("{x}", data[str(counter)])
                    counter += 1
                if "top.png" in line:
                    line = line.replace("top.png", os.path.join(os.getcwd(), "top.png"))
                if "bottom.png" in line:
                    line = line.replace("bottom.png", os.path.join(os.getcwd(), "bottom.png"))
                lines.append(line)

        with tempfile.TemporaryDirectory() as tmpdir:
            filename = form.replace(".json", ".tex")
            with open(os.path.join(tmpdir, filename), "w") as f:
                f.writelines(lines)
            cmd = ["pdflatex", filename]
            subprocess.check_call(cmd, shell=False, cwd=tmpdir)
            subprocess.check_call(cmd, shell=False, cwd=tmpdir)
            result = form.replace(".json", ".pdf")
            shutil.move(os.path.join(tmpdir, result), os.path.join(os.getcwd(), result))

main()
