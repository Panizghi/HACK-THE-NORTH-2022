# HACK-THE-NORTH-2022

*TEMP TITLE* Fire Away - Using ML Models and Arduino to Design Aerial Firefighters

Hello, our names are Paniz, Kevin, Laurence, and Ian, and we are the innovation team behind this creation. Fire Away is meant as a portable solution for quick fire detection and resolution. We are working with ML, AI, Arduino, ESP, DJI, Litchi, and more to deliver this project.

Drone

Hardware

Software

## Quickstart

Install dependencies.

```
pip install -r requirements.txt
```

Set API key for Assembly AI (speech to text API):
```
set AAI_API_KEY=<API key>
```

Start server

```
python app.py
```

Start clients
```
python -m src.client_socket_opencv
python -m src.client_socket_sdk_controller
python -m src.client_socket_speech
```

`src/client_socket_sdk_controller.py` controls the Drone. Include the code under the `while True` loop block.

`server_data` is a dictionary variable with the commands:
```
{"data": {"commandVector": {"direction":"hover", "magnitude":0, "predictedClass":"stop"}}}
```

Choices of direction:

* `front`
* `back`
* `left`
* `right`
* `top`
* `bottom`
* `rotate_left`
* `rotate_right`

Go to localhost port `8000`.
