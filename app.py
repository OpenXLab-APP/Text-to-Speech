# Copyright (c) 2023 Amphion.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import subprocess

command_to_run = "cd ./modules/monotonic_align;mkdir -p monotonic_align;python setup.py build_ext --inplace;cd /home/user/app"

try:
    result = subprocess.check_output(command_to_run, shell=True, text=True)
    print("Command output:")
    print(result)
except subprocess.CalledProcessError as e:
    print(f"Command failed with return code {e.returncode}")

import gradio as gr
import os
import inference

SUPPORTED_SPEAKERS = {
    "92":"hifitts_92",
    "6097":"hifitts_6097",
    "6670":"hifitts_6670",
    "6671":"hifitts_6671",
    "8051":"hifitts_8051",
    "9017":"hifitts_9017",
    "9136":"hifitts_9136",
    "11614":"hifitts_11614", 
    "11697":"hifitts_11697",
    "12787":"hifitts_12787" 
}


def tts_inference(
    input_text,
    target_speaker
):

    args_list = ["--config", "./egs/tts/vits_hifitts/exp_config.json"]
    args_list += ["--checkpoint_path", "./latest-checkpoint"]
    args_list += ["--speaker_name", target_speaker]
    args_list += ["--text", input_text]
    args_list += ["--mode","single"]
    args_list += ["--output_dir", "result"]
    args_list += ["--log_level", "debug"]

    os.environ["WORK_DIR"] = "./"
    inference.main(args_list)

    ### Display ###
    result_file = os.path.join(
        "result/{}.wav".format(target_speaker)
    )
    return result_file


demo_inputs = [
    gr.Textbox(
        label="Input text",
        type="text",
        lines=1,
        max_lines=20
    ),
    gr.Radio(
        choices=list(SUPPORTED_SPEAKERS.keys()),
        label="Target Speaker",
        value="92"
    )
]

demo_output = gr.Audio(label="")



demo = gr.Interface(
    fn=tts_inference,
    inputs=demo_inputs,
    outputs=demo_output,
    title="Amphion HifiTTS Text-to-Speech Demo",
)

if __name__ == "__main__":
    demo.launch(share=True)