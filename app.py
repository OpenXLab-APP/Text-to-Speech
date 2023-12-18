# Copyright (c) 2023 Amphion.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree

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
    "Cori Samuel":"hifitts_92",
    "Phil Benson":"hifitts_6097",
    "John Van Stan":"hifitts_6670",
    "Mike Pelton":"hifitts_6671",
    "Tony Oliva":"hifitts_8051",
    "Maria Kasper":"hifitts_9017",
    "Helen Taylor":"hifitts_9136",
    "Sylviamb":"hifitts_11614", 
    "Celine Major":"hifitts_11697",
    "LikeManyWaters":"hifitts_12787" 
}


def tts_inference(
    input_text,
    target_speaker
):
    ### Target Speaker ###
    target_speaker = SUPPORTED_SPEAKERS[target_speaker]
    
    args_list = ["--config", "./egs/tts/vits_hifitts/exp_config.json"]
    args_list += ["--checkpoint_path", "./ckpt/latest-checkpoint"]
    args_list += ["--speaker_name", target_speaker]
    args_list += ["--text", input_text]
    args_list += ["--mode","single"]
    args_list += ["--output_dir", "result"]
    args_list += ["--log_level", "debug"]

    os.environ["WORK_DIR"] = "./"
    inference.main(args_list)

    ### Display ###
    result_file = os.path.join(
        "result/single/test_pred.wav"
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