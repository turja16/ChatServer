# Messaging application

## Overview

The Simple Chat Application is a basic client-server program that enables real-time text messaging between multiple clients through a central server. It uses the TCP/IP protocol for communication, ensuring reliable data transmission. Clients can connect to the server, send messages, and receive messages from other connected clients. The server acts as an intermediary, forwarding messages according to the clients' requests.

## Features

- Real-time Messaging: Instantly send and receive messages between clients.
- Server-Client Architecture: Utilizes a server-client model for handling communication.
- Multi Threaded server implemented by Python 
- Clean Shutdown: Provides a mechanism for clients to exit the conversation gracefully.

## Requirements

- Python 3.x

## How to Run 
1. In terminal execute shell script by --- sh run.sh

### Server

1. If you run explicitly, Run the server using the command: `python server.py <Server addr> <Server port> <number of clients>`.
2. The server will automatically select an available port and display it in the console.
3. Server will automaticall start given number of clients client terminal from code

### Client

1. Server will automaticall start given number of clients client terminal from code. If you want to run explicitly Use the command: `python client.py <Server addr>  <ServerPort>`.
2. Follow the on-screen prompts to send and receive messages.

## Usage

- Upon connecting to the server, clients can send messages to other connected clients through server.




