# IotDeviceSimulator
Dispositivos IoT simulados hechos en Python, permite enviar datos diferentes proveedores de cloud computing y servicios de administracion de dispositivos IoT.

## Que necesitamos
Para poder ejecutar los dispositivos IoT reaizar los siguientes pasos.

1. Clonar el repositorio
```bash
git clone https://github.com/BryanAvalos23/IotDeviceSimulator.git
```
2. Dependiendo la plataforma deberas utilizar certificados o algun tipo de topic. en caso de conectarnos a AWS debemos descargar cada certificado y adjuntar las politicas que necesitamos en nuestro archivo
3. Para las politicas del dispositivo para poder conectarnos debemos conectar esto. Permitira la conexion a nuestro servicio en la nube.
```bash
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Publish",
        "iot:Receive",
        "iot:PublishRetain"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Subscribe"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Connect"
      ],
      "Resource": "*"
    }
  ]
}
```
