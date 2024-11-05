from dotenv import load_dotenv
load_dotenv("data/.env")
import logging
from datetime import datetime
from dotenv import load_dotenv
from retry import retry
load_dotenv("data/.env")
import numpy as np
from PIL import Image
import argparse
import torch
import json
import requests
from PIL import Image
from io import BytesIO
import re
import os
import tqdm
import base64
import glob
import google.generativeai as genai

genai.configure(api_key=os.environ.get("Gemini_API_KEY"))

def call_gemini(question_text, image_path, model_name="gemini-1.5-flash"):
    model = genai.GenerativeModel(model_name)
    image_file = genai.upload_file(image_path)
    result = model.generate_content(
        [image_file, "\n\n", question_text]
    )
    return result.text
#####

class Experiment:
    def __init__(self, experiment_path):
        self.experiment_path = experiment_path
        self.question_path = os.path.join(experiment_path, 'question.txt')
        self.answer_path = os.path.join(experiment_path, 'answer.txt')
        self.model_response_path = os.path.join(experiment_path, 'model_response.txt')
        self.media_paths = self._get_media_paths()
        logging.debug(f"Initialized Experiment object for: {self.experiment_path}")
    def _get_media_paths(self):
        media_dir = os.path.join(self.experiment_path, 'media')
        media_files = []
        if os.path.exists(media_dir) and os.path.isdir(media_dir):
            media_files = [
                os.path.join(media_dir, file)
                for file in sorted(os.listdir(media_dir))
            ]
            logging.debug(f"Media files found in {media_dir}: {media_files}")
        else:
            logging.warning(f"No media directory found at {media_dir}")
        return media_files

    def read_question(self):
        try:
            with open(self.question_path, 'r', encoding='utf-8') as f:
                question_text = f.read()
            return question_text
        except FileNotFoundError:
            logging.error(f"Question file not found: {self.question_path}")
            return None

    def read_answer(self):
        try:
            with open(self.answer_path, 'r', encoding='utf-8') as f:
                answer_text = f.read()
            return answer_text
        except FileNotFoundError:
            logging.error(f"Answer file not found: {self.answer_path}")
            return None

    def read_model_response(self):
        try:
            with open(self.model_response_path, 'r', encoding='utf-8') as f:
                answer_text = f.read()
            return answer_text
        except FileNotFoundError:
            logging.error(f"Answer file not found: {self.model_response_path}")
            return None

    def write_model_response(self, response_text):
        try:
            with open(self.model_response_path, 'w', encoding='utf-8') as f:
                f.write(response_text)
            return True
        except Exception as e:
            logging.error(f"Error writing model response to file: {self.model_response_path}, {e}")
            return False

def find_experiments(base_path):
    experiments = []
    for experiment_dir in os.listdir(base_path):
        experiment_path = os.path.join(base_path, experiment_dir)
        if os.path.isdir(experiment_path):
            logging.info(f"Found experiment directory: {experiment_path}")
            experiment_obj = Experiment(experiment_path)
            experiments.append(experiment_obj)
        else:
            logging.debug(f"Skipped non-directory item: {experiment_path}")
    return experiments

def main():
    parser = argparse.ArgumentParser(description="Iterate over experiment folders and create Experiment objects.")
    parser.add_argument('--dir', type=str, required=True, help="Path to the directory containing experiments.")
    args = parser.parse_args()
    # Step 1: Create a logging directory if it doesn't exist
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    # Step 2: Create a unique log file name based on the current date and time
    log_filename = datetime.now().strftime('log_%Y-%m-%d_%H-%M-%S.log')
    log_filepath = os.path.join(log_dir, log_filename)
    # Step 3: Configure the logging module
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
        handlers=[
            logging.FileHandler(log_filepath),  # Log to the file
            # logging.StreamHandler()  # Optionally log to the console
        ]
    )
    base_path = args.dir
    logging.info(f"Starting to process experiments in base directory: {base_path}")
    if not os.path.exists(base_path):
        logging.error(f"The specified directory does not exist: {base_path}")
        return
    experiment_list = find_experiments(base_path)
    logging.info(f"Total experiments found: {len(experiment_list)}")
    # Process each experiment: print out the details and contents of question and answer files
    for exp in experiment_list:
        logging.info(f"Processing Experiment: {exp.experiment_path}")
        question_text = exp.read_question()
        if question_text is not None:
            logging.info(f"Question Text:\n{question_text}")
        else:
            logging.warning(f"Could not read question text for {exp.experiment_path}")
        answer_text = exp.read_answer()
        if answer_text is not None:
            logging.info(f"Answer Text:\n{answer_text}")
        else:
            logging.warning(f"Could not read answer text for {exp.experiment_path}")
        model_response = exp.read_answer()
        if model_response is not None:
            logging.info(f"Model Response Text:\n{model_response}")
        else:
            logging.warning(f"Could not read answer text for {exp.experiment_path}")
        logging.info("Media Files:")
        for media_path in exp.media_paths:
            logging.info(f" - {media_path}")
        logging.info("")

    # query GPT models
    for exp in experiment_list:
        logging.info(f"Large Language Model query:{exp.experiment_path}")
        question_text = exp.read_question()
        media = exp.media_paths

        try:
            print(f"Quering Experiment: {exp.experiment_path}")
            output = call_gemini(question_text, media[0], 'gemini-1.5-flash')
        except:
            logging.info(f"Failed Experiment: {exp.experiment_path}")
            print(f"Failed Experiment: {exp.experiment_path}")
            print(f"Failed Experiment: {exp.media_paths}")
        exp.write_model_response(output)

if __name__ == "__main__":
    main()
