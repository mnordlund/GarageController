# Garage Controller

A remote controller using an android phone and a raspberry pi to control a garagedoor.

## Description and system overview

The system consists of two main parts an Android Application and a Raspberry PI software. These softwares communicate using a [Firebase](https://firebase.google.com/) Realtime Database.

The Raspberry PI is connected to a set of modules, via GPIO, to control and check the status of the garage door.

The android application shows the status and is able to operate and lock the garage door.

When the lock is active no clients are able to operate the door until the lock has been release by a client.

For more detailed information:

- [Android Application](Android/README.md)
- [Raspberry Software](raspberry/README.md)

## Modules

The modules I used are arduino sensors and parts of the [Big Playknowlogy module package](https://www.kjell.com/se/produkter/el-verktyg/arduino/moduler/playknowlogy-stora-modul-paketet-for-arduino-p87291)

To be able to use some of the 5v modules with the Raspberry Pi 3.3v GPIO a [level shifter](https://www.amazon.se/dp/B07RY15XMJ/ref=pe_24982401_503747021_TE_SCE_dp_2) is used.

### Mini reed sensor

The mini reed sensor, together with a strong natural magnet attached to the garage door, is used to detect if the door is fully closed.

### Dual ultrasonic sensor module

The dual ultrasonic sensor module is mounted in the roof above where the opened door ends up and measures down to detect either the door, if it is opened, the car, if it is in the garage, or the floor if nothing is blocking it. The distance to the nearest object is used to determine the status. Thus the car cannot be detected if the door is opened.

## Firebase realtime database setup

The realtime data base has a schema that is defined as:

```JSON
{
  "commands" : {
    "lock" : false,
    "operate" : false
  },
  "status" : {
    "carInGarage" : true,
    "doorClosed" : true,
    "doorOpened" : false,
    "locked" : false
  }
}
```

### Commands

|         |                                                                                         |
| ------- | --------------------------------------------------------------------------------------- |
| lock    | Locks the door so that no client can operate the door, without first disabling the lock |
| operate | Operates the door, i.e closes or opens the door depending on the status of the door     |

### status

|             |                                   |
| ----------- | --------------------------------- |
| carInGarage | Is there a car in the garage      |
| doorClosed  | Is the door fully closed          |
| doorOpened  | Is the door fully opened          |
| locked      | Is the door locked by any clients |

## Thirdparty software and resources

<div>Application icon made by <a href="https://www.flaticon.com/authors/talha-dogar" title="Talha Dogar">Talha Dogar</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>