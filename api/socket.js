import { createServer } from "net";

const server = createServer((socket) => {
  console.log("Client connected");

  socket.on("data", (data) => {
    const message = data.toString().trim();
    console.log("Received from Python:", message);
    // Process the serial data her
  });

  socket.on("close", () => {
    console.log("Client disconnected");
  });
});

server.listen(4435, () => {
  console.log("Bun.js TCP server listening on port 4435");
});
