import os
import argparse
import anthropic

# Replace 'YOUR_API_KEY' with your actual Anthropic API key
client = anthropic.Client(api_key='YOUR_API_KEY')

# Base directory of your experiments
BASE_DIR = 'path_to_your_repository'  # Update this path

# List of valid cognitive tasks
COGNITIVE_TASKS = [
    'Mechanical_Reasoning',
    'Perspective_Taking',
    'Law_of_Conservation'
]

def process_experiment(task, experiment):
    task_dir = os.path.join(BASE_DIR, task)
    if not os.path.isdir(task_dir):
        print(f"Task directory not found: {task_dir}")
        return

    exp_dir = os.path.join(task_dir, experiment)
    if not os.path.isdir(exp_dir):
        print(f"Experiment directory not found: {exp_dir}")
        return

    question_file = os.path.join(exp_dir, 'question.txt')
    answer_file = os.path.join(exp_dir, 'correct_answer.txt')
    media_dir = os.path.join(exp_dir, 'media')

    if not os.path.isfile(question_file) or not os.path.isfile(answer_file):
        print(f"Question or answer file missing in {exp_dir}")
        return

    # Read question and correct answer
    with open(question_file, 'r', encoding='utf-8') as qf:
        question = qf.read().strip()
    with open(answer_file, 'r', encoding='utf-8') as af:
        correct_answer = af.read().strip()

    # Load media files
    media_files = []
    if os.path.isdir(media_dir):
        for media_file in sorted(os.listdir(media_dir)):
            media_path = os.path.join(media_dir, media_file)
            if os.path.isfile(media_path):
                media_files.append(media_path)
    else:
        print(f"No media directory found in {exp_dir}")

    # Since Anthropic API does not support image inputs, we'll mention the media files in the prompt
    media_descriptions = ''
    if media_files:
        media_descriptions = ' [Note: The following images are associated with the question but cannot be displayed: '
        media_descriptions += ', '.join([os.path.basename(f) for f in media_files]) + ']'

    # Construct the prompt
    prompt = f"{anthropic.HUMAN_PROMPT} You are a helpful assistant that answers questions based on provided text and descriptions of images.{media_descriptions}\n\nQuestion: {question}\n{anthropic.AI_PROMPT}"

    # Send the question to the Anthropic API
    assistant_reply = get_model_response(prompt)

    # Prepare the output text
    output_text = f"Task: {task}, Experiment: {experiment}\n"
    output_text += f"Question:\n{question}\n\n"
    output_text += f"Model's Response:\n{assistant_reply}\n\n"
    output_text += f"Correct Answer:\n{correct_answer}\n\n"

    # Compare the model's response to the correct answer
    comparison_result = compare_answers(assistant_reply, correct_answer)
    output_text += f"{comparison_result}\n"
    output_text += "-" * 50 + "\n"

    # Print the output
    print(output_text)

    # Save the output to model_answer.txt in the experiment directory
    model_answer_file = os.path.join(exp_dir, 'model_answer.txt')
    with open(model_answer_file, 'w', encoding='utf-8') as f:
        f.write(output_text)

def get_model_response(prompt):
    # Call the Anthropic API
    response = client.completion(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        max_tokens_to_sample=1000,
        model="claude-v1"  # Use the appropriate model name
    )

    assistant_reply = response['completion'].strip()
    return assistant_reply

def compare_answers(model_response, correct_answer):
    # Simple comparison (can be enhanced)
    if model_response.lower() == correct_answer.lower():
        return "The model's response matches the correct answer."
    else:
        return "The model's response does not match the correct answer."

def main():
    parser = argparse.ArgumentParser(description='Process a specific cognitive task experiment.')
    parser.add_argument('task', type=str, help='The cognitive task (e.g., Mechanical_Reasoning)')
    parser.add_argument('experiment', type=str, help='The experiment folder (e.g., Experiment_1)')
    args = parser.parse_args()

    task = args.task
    experiment = args.experiment

    if task not in COGNITIVE_TASKS:
        print(f"Invalid task. Available tasks are: {', '.join(COGNITIVE_TASKS)}")
        return

    process_experiment(task, experiment)

if __name__ == "__main__":
    main()