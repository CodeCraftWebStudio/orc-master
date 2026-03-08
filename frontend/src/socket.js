import { io } from "socket.io-client";

const URL = "https://orc-backend.onrender.com";

const socket = io(URL, {
  withCredentials: true,
});

export default socket;
