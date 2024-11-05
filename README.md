# Vision Language Model Cognitive Experiments

This repository contains cognitive experiments designed to evaluate Vision Language Models (VLMs) on cognitive task conditions.

Each cognitive task is organized into its own directory, containing a series of experiments labeled sequentially.

## Repository Structure

```
├── Task_Condition/
│   ├── Experiment_1/
│   │   ├── question.txt
│   │   ├── answer.txt
│   │   ├── model_response.txt
│   │   └── media/
│   │       ├── 1
│   │       ├── 2
│   │       └── 3
│   ├── Experiment_2/
│   │   └── ...
│   └── ...
├── Perspective_Taking/
├── Law_of_Conservation/
├── infer_code
└── README.md
```

## Experiment Structure
Each experiment follows the same structure:

### question.txt: 
Contains the question posed to the VLM.
### correct_answer.txt: 
Contains the expected correct answer.
### media/: 
A folder containing all necessary media files for the experiment, labeled numerically (e.g., 1, 2, 3).
### Cognitive Tasks
- Adjust according to the investigator's needs. 

## How to Use

Run code, 
```
python gpt.py --dir data/GPT_Experiment_Mechanical_Reasoning
```

Clean repo,
```
find . -name ".DS_Store" -delete       
```

Resize,
```
python resize.py       
```

Push results to github
```
git add '**/answer.txt' '**/model_response.txt'
git commit -m "Add all question.txt and model_response.txt files"
```

Make all other media files into single image files
```
python mov2png.py
```

Check accuracy using Gemini
```
python gemini-as-the-judge.py --dir ./data/dezhi_special
```

- Navigate to the desired cognitive task directory (e.g., Mechanical_Reasoning).
- Select an experiment folder (e.g., Experiment_1).
- Read the question.txt file to understand the task.
- Review the media files in the media/ folder as necessary for the experiment.
- Compare the VLM's output to the correct_answer.txt to evaluate performance.

License
This project is licensed under the Creative Commons NC

Contact
For questions or suggestions, please open an issue or contact growing.ai.like.a.child@gmail.com
