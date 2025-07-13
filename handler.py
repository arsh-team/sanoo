from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch
import base64
import io

# Load processor and model
processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-3B-Instruct")
model = AutoModelForVision2Seq.from_pretrained("Qwen/Qwen2.5-VL-3B-Instruct").cuda()
model.eval()

# Handler function
def handler(event):
    inputs = event["input"]
    prompt = inputs.get("prompt", "")
    image_list = inputs.get("images", [])

    if not image_list:
        return {"error": "No images provided"}
    if len(image_list) > 100:
        return {"error": "Maximum 100 images supported per request"}

    results = []

    for idx, img_b64 in enumerate(image_list):
        try:
            image_data = base64.b64decode(img_b64)
            image = Image.open(io.BytesIO(image_data)).convert("RGB")

            model_inputs = processor(text=prompt, images=image, return_tensors="pt").to("cuda")
            output = model.generate(**model_inputs, max_new_tokens=512)
            decoded = processor.batch_decode(output, skip_special_tokens=True)[0]

            results.append({"index": idx, "output": decoded})
        except Exception as e:
            results.append({"index": idx, "error": str(e)})

    return {"results": results}
