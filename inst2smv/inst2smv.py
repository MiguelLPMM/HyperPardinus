import argparse
from inst2smv_ah import inst2smv_ah
from inst2smv_hq import inst2smv_hq
import os

def main():
    parser = argparse.ArgumentParser(description="Read from a file and write its contents to another file.")
    parser.add_argument("flag", choices=["ah", "hq"], help="Flag to determine the input file path.")
    parser.add_argument("--dir", help="Path to the directory containing input files.")
    parser.add_argument("--stem", help="Stem name for the files.")

    parser.add_argument("--cex", default="cex.ah")
    parser.add_argument("--qcir", default="build_today/HQ.qcir")
    parser.add_argument("--quabs", default="build_today/HQ.quabs")

    args = parser.parse_args()

    run_dir = os.path.abspath(args.dir)

    # Determine the input file path based on the flag
    if args.flag == "ah":
        inst2smv_ah(
            run_dir=run_dir,
            input_ah=os.path.join(run_dir, args.cex),
            stem=args.stem,
        )

    elif args.flag == "hq":
        inst2smv_hq(
            run_dir=run_dir,
            input_qcir=os.path.join(run_dir, args.qcir),
            input_quabs=os.path.join(run_dir, args.quabs),
            stem=args.stem,
        )

if __name__ == "__main__":
    main()