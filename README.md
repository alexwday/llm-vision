# LLM Vision

A simple project for testing the Qwen 2 VL model with a hosted API endpoint.

## Setup

1. Place test images in the `llm_vision/data/images/` directory
2. Open `test_qwen.ipynb` in Jupyter
3. Update the `API_URL` with your endpoint
4. Run the notebook cells to test the model

## Structure

- `test_qwen.ipynb`: Jupyter notebook for testing the model
- `llm_vision/`: Package directory
  - `data/images/`: Directory for test images

## Usage

The notebook contains helper functions to:
- Encode images as base64
- Send requests to the API
- Display images and model responses

You can customize the prompts and test different images to explore the model's capabilities.