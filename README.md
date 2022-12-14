# HACK-THE-NORTH-2022

<img width="1491" height="40%" alt="Screen Shot 2022-09-18 at 5 44 21 AM" src="https://user-images.githubusercontent.com/90856064/190896042-bf9b068d-3bce-45ef-94d4-a443fd22204b.png">


## Fire Away - Using ML Models and Arduino to Design Aerial Firefighters

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
* `up`
* `down`
* `rotate_left` or `turn_left`
* `rotate_right` or `turn_right`

Go to localhost port `8000`.
