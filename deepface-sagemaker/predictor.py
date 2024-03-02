"""
Implement sagemaker compatible flask app for deepface.
Based on https://github.com/serengil/deepface/blob/master/deepface/api/src/modules/core/routes.py. 
"""
import logging
import json

import flask
from flask import Flask, Response
from deepface import DeepFace
from deepface.api.src.modules.core import service

logger = logging.getLogger()
logger.setLevel("INFO")

# The flask app for serving predictions
app = Flask(__name__)

# Load weights for default model.
model = DeepFace.build_model("VGG-Face")

def represent(input_args):
    if input_args is None:
        return {"message": "empty input set passed"}

    img_path = input_args.get("img") or input_args.get("img_path")
    if img_path is None:
        return {"message": "you must pass img_path input"}

    model_name = input_args.get("model_name", "VGG-Face")
    detector_backend = input_args.get("detector_backend", "opencv")
    enforce_detection = input_args.get("enforce_detection", True)
    align = input_args.get("align", True)

    obj = service.represent(
        img_path=img_path,
        model_name=model_name,
        detector_backend=detector_backend,
        enforce_detection=enforce_detection,
        align=align,
    )

    logger.debug(obj)

    return obj


def verify(input_args):
    if input_args is None:
        return {"message": "empty input set passed"}

    img1_path = input_args.get("img1") or input_args.get("img1_path")
    img2_path = input_args.get("img2") or input_args.get("img2_path")

    if img1_path is None:
        return {"message": "you must pass img1_path input"}

    if img2_path is None:
        return {"message": "you must pass img2_path input"}

    model_name = input_args.get("model_name", "VGG-Face")
    detector_backend = input_args.get("detector_backend", "opencv")
    enforce_detection = input_args.get("enforce_detection", True)
    distance_metric = input_args.get("distance_metric", "cosine")
    align = input_args.get("align", True)

    verification = service.verify(
        img1_path=img1_path,
        img2_path=img2_path,
        model_name=model_name,
        detector_backend=detector_backend,
        distance_metric=distance_metric,
        align=align,
        enforce_detection=enforce_detection,
    )

    logger.debug(verification)

    return verification


def analyze(input_args):
    if input_args is None:
        return {"message": "empty input set passed"}

    img_path = input_args.get("img") or input_args.get("img_path")
    if img_path is None:
        return {"message": "you must pass img_path input"}

    detector_backend = input_args.get("detector_backend", "opencv")
    enforce_detection = input_args.get("enforce_detection", True)
    align = input_args.get("align", True)
    actions = input_args.get("actions", ["age", "gender", "emotion", "race"])

    demographies = service.analyze(
        img_path=img_path,
        actions=actions,
        detector_backend=detector_backend,
        enforce_detection=enforce_detection,
        align=align,
    )

    logger.debug(demographies)

    return demographies


@app.route("/ping", methods=["GET"])
def ping():
    # Check if the classifier was loaded correctly
    health = model is not None
    status = 200 if health else 404
    return Response(response="\n", status=status, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def transformation():
    input_json = flask.request.get_json()
    deepface_service = input_json["service"]

    if deepface_service == "analyze":
        response = analyze(input_json)
    elif deepface_service == "verify":
        response = verify(input_json)
    elif deepface_service == "represent":
        response = represent(input_json)
    else:
        return Response(
            response={
                "message": f"Unsupported service: {deepface_service}."
                "Allowed values: 'analyze', 'verify', 'represent'."
            },
            status=404,
            mimetype="application/json",
        )

    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
