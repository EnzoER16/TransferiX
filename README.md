# TransferiX

<div align="center">
  <img src="assets/icon.ico" width="160" height="160"/>
</div>

Transferix is a file transfer application built using Python. It allows users to easily transfer files between devices over a local network.

## Features

* **Automatic Device Discovery:** Uses UDP *broadcast discovery* to instantly find other devices on your local network that are running TransferiX.
* **Stable and Direct Transfer:** Implements file transfers over TCP sockets, ensuring fast data transmission within the local network.
* **Drag & Drop Support:** Integrates drag-and-drop functionality using `tkinterdnd2` and `CustomTkinter`, making file selection easy on desktop systems.

> [!NOTE]
> **Current Availability:**
> * This tool is currently available for **Windows**.
> * **Android** support is currently in the testing phase.

> [!CAUTION]
> **Network and Firewall Considerations:**
> Since TransferiX uses local ports to discover devices and receive files, the Windows Firewall will prompt you for permissions the first time you run the program. Please keep the following in mind when using the app:
> * **Trusted Networks (Personal Use):** For everyday use on a home network or connected to your phone's hotspot *(tested)*, there shouldn't be any issues. You can choose to check the "Public networks" box in the firewall prompt upon startup, provided you trust the network you are connected to.
> * **Untrusted Networks:** If you do not trust the network, we recommend not checking the box. Instead, go to your system settings and ensure your current Wi-Fi connection is set to Private Network.
> * **Unencrypted Transfers:** Currently, files are sent without encryption. Anyone actively monitoring the network traffic could potentially intercept the data. Please avoid transferring sensitive or confidential information.
> * **Security Note:** It is advised not to use the app or enable these permissions on "real public networks" (such as cafes, airports, etc.).