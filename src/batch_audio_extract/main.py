# -*- coding: utf-8 -*-
# ###################################################################################
#
#             Your text
#
#    License:
#    Author:
#
#                    __   .__
#      _____ _____  |  | _|__|_  _  _______ ____________
#     /     \\__  \ |  |/ /  \ \/ \/ /\__  \\_  __ \__  \
#    |  Y Y  \/ __ \|    <|  |\     /  / __ \|  | \// __ \_
#    |__|_|  (____  /__|_ \__| \/\_/  (____  /__|  (____  /
#          \/     \/     \/                \/           \/
#
#    Program walks through a directory (and subs), watch for audio and
#   extract an excerpt save the new file
#
# ######################################################################



import argparse
from pathlib import Path



from batch_audio_extract.process import process


def main():
    parser = argparse.ArgumentParser(
        description="Extracts audio excerpts from audio files."
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug mode."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input directory containing audio files.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output directory for extracted audio files.",
    )
    parser.add_argument(
        "-s",
        "--start",
        type=int,
        help="Starting second for the audio excerpt.",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=int,
        help="Ending second for the audio excerpt.",
    )
    parser.add_argument(
        "-f",
        "--fade",
        type=int,
        help="Fade duration in seconds (0 for no fade).",
    )

    args = parser.parse_args()

    input_params = {}
    if args.debug:
        input_params["debug"] = True
    if args.input:
        input_params["input_dir"] = Path(args.input)
    if args.output:
        input_params["output_dir"] = Path(args.output)
    if args.start is not None:
        input_params["first_second"] = args.start
    if args.end is not None:
        input_params["last_second"] = args.end
    if args.fade is not None:
        input_params["fade_d"] = args.fade

    
    process(input_params=input_params)
  



if __name__ == "__main__":
    main()