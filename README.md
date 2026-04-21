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
> 
> * **Standard Home Networks:** For everyday use on a trusted home network, simply checking the "Private networks" box in the firewall prompt is sufficient.
> * **Mobile Hotspots (Special Case):** When connecting your Windows PC to a mobile phone's hotspot, Windows automatically classifies it as a "Public" network by default. For the app to work in this scenario, you must do one of the following:
>   * Check the "Public networks" box in the firewall prompt upon startup (only do this if it is your own trusted hotspot).
>   * Alternatively, do not check the box, but go to your Windows Wi-Fi settings and manually change the hotspot's network profile from Public to **Private Network**.
> * **Unencrypted Transfers:** Currently, files are sent without encryption. Anyone actively monitoring the network traffic could potentially intercept the data. Please avoid transferring sensitive or confidential information.
> * **Security Note:** It is strongly advised not to use the app or enable public network permissions on actual, untrusted public networks (such as cafes, airports, university campuses, etc.).